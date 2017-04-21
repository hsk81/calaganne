# Libbitcoin: bx ec-to-public

 --- *Don't trust a man who needs an income -- except if it is minimum wage. Those in corporate captivity would do anything to "feed a family".* [[NNT]]

![Generator G multiplied 8 times over an Elliptic curve][ECMUL]

Today, I'd like to talk about how to derive a *public* key from a *secret* using [Elliptic Curve Cryptography][ECC]. Let's try the following command `bx ec-to-public`:

```
hsk81 ~ $ bx ec-to-public -h

Usage: bx ec-to-public [-hu] [--config value] [EC_PRIVATE_KEY]           

Info: Derive the EC public key of an EC private key. Defaults to the     
compressed public key format.                                            

Options (named):

-c [--config]        The path to the configuration settings file.        
-h [--help]          Get a description and instructions for this command.
-u [--uncompressed]  Derive using the uncompressed public key format.    

Arguments (positional):

EC_PRIVATE_KEY       The Base16 EC private key. If not specified the key 
                     is read from STDIN. 
```

Alright, apparently `ec-to-public` takes secret and turns it into something public, allowing other people to encrypt messages, which only you the holder of the secret can decrypt. That's at least the working assumption under which public key cryptography operates!

In the context of Bitcoin the public key can be used as your address people can send "money" to, and only you can spend them, since as a holder of the private key only you can sign the associated transactions.

So, let's generate such a public address for other people to send us money:
```
hsk81 ~ $ bx seed | bx ec-new | bx ec-to-public
03e81a84fe1d5aa4269b0faa78110549caf3873364467688dec27c94761c2b1e6e
```

Well, this does not really look like the traditional Bitcoin address you would expect so see -- for example:
```
12AEJmWva5QJVYmQ3r3vdFZeFfLUeSVPBq
```

But that conversion from a public key to an actual address (accomplished with `bx ec-to-address`) will be discussed in depth in another post. Here, we want to focus on how exactly this "magic" transformation from a private key (secret) to a public key (address) is accomplished.

Let's dive directly into the code of the `bx ec-to-public` command:

```cpp
console_result ec_to_public::invoke(
    std::ostream& output, std::ostream& error)
{
    const auto& secret = get_ec_private_key_argument();
    const auto& uncompressed = get_uncompressed_option();

    ec_compressed point;
    secret_to_public(point, secret);

    output << ec_public(point, !uncompressed) << std::endl;
    return console_result::okay;
}
```

As we see, some `secret` is transformed to a public `point`, which is called so because it corresponds to an actual "point" in [Elliptic curve cryptography][ECC]. The short explanation of how this is achieved, is to note that the `secret` is like the number of multiplications of the `point` over Elliptic Curves, and the *NSA* telling us that this multiplication is "secure" enough to operate a multi-billion economy. Let's see, where we will end up...

Anyway, since there is a bunch of "independent" mathematicians telling us more or less the same story, that ECC is secure enough (under the assumption that *one-way* functions exist, **and** under the assumption that $P\neq{NP}$ in a Turing model of computation, **and** under the assumption that current Quantum computers are *not* able to brute force the `secret` from the public `point` -- lot's of assumptions), we believe what we're told and move on with our technical discussion.

Alright, let's have a look at the `secret_to_public` function:
```cpp
bool secret_to_public(ec_compressed& out, const ec_secret& secret)
{
    const auto context = signing.context();
    return secret_to_public(context, out, secret);
}
```

So, apparently what we do is to turn the `secret` under a certain signing `context` (which I will not further elaborate) into something public --
 represented here by the `out` reference. Let's dive deeper:
```cpp
template <size_t Size>
bool secret_to_public(
    const secp256k1_context* context,
    byte_array<Size>& out, const ec_secret& secret)
{
    secp256k1_pubkey pubkey;
    return secp256k1_ec_pubkey_create(
        context, &pubkey, secret.data()) == 1 &&
        serialize(context, out, pubkey);
}
```

We're getting close to the truth, and the magic seems to become more and more profane: Apparently, the `secp256k1_ec_pubkey_create` function seems to be doing the hard job, and if everything goes fine (`== 1`), we serialize the `pubkey` to `out`. Let's dive even further:

```c
int secp256k1_ec_pubkey_create(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const unsigned char *seckey)
{
    secp256k1_gej pj;
    secp256k1_ge p;
    secp256k1_scalar sec;
    int overflow;
    int ret = 0;
    VERIFY_CHECK(ctx != NULL);
    ARG_CHECK(pubkey != NULL);
    memset(pubkey, 0, sizeof(*pubkey));
    ARG_CHECK(secp256k1_ecmult_gen_context_is_built(&ctx->ecmult_gen_ctx));
    ARG_CHECK(seckey != NULL);

    secp256k1_scalar_set_b32(&sec, seckey, &overflow);
    ret = (!overflow) & (!secp256k1_scalar_is_zero(&sec));
    if (ret) {
        secp256k1_ecmult_gen(&ctx->ecmult_gen_ctx, &pj, &sec);
        secp256k1_ge_set_gej(&p, &pj);
        secp256k1_pubkey_save(pubkey, &p);
    }
    secp256k1_scalar_clear(&sec);
    return ret;
}
```

And welcome to the funny world of `C` programmers, who are not able to come up with reasonable variable names: The code above is actually *not* part of the `libbitcoin` software (which is currently maintained by [Eric Voskuil][evoskuil] using his beautiful `C++`).

Alright, let's deconstruct the gibberish above and understand what's going on: Well, this code does not do actually much except taking the input arguments, doing some sanity checks and invoking then the `secp256k1_ecmult_gen` function, which does the "heavy" lifting -- namely executing a `sec` number of times an addition over Elliptic curves (modulo some prime number), which is then saved to `pj`, which is then turned into `p`, which is then finally stored in the `pubkey` pointer.

So, what does `secp256k1_ecmult_gen` really do? Let's see:
```c
static void secp256k1_ecmult_gen(
    const secp256k1_ecmult_gen_context *ctx,
    secp256k1_gej *r, const secp256k1_scalar *gn)
{
    secp256k1_ge add;
    secp256k1_ge_storage adds;
    secp256k1_scalar gnb;
    int bits;
    int i, j;
    memset(&adds, 0, sizeof(adds));
    *r = ctx->initial;
    /* Blind scalar/point multiplication by
       computing (n-b)G + bG instead of nG. */
    secp256k1_scalar_add(&gnb, gn, &ctx->blind);
    add.infinity = 0;
    for (j = 0; j < 64; j++) {
        bits = secp256k1_scalar_get_bits(
            &gnb, j * 4, 4
        );
        for (i = 0; i < 16; i++) {
            secp256k1_ge_storage_cmov(
                &adds, &(*ctx->prec)[j][i], i == bits
            );
        }
        secp256k1_ge_from_storage(&add, &adds);
        secp256k1_gej_add_ge(r, r, &add);
    }
    bits = 0;
    secp256k1_ge_clear(&add);
    secp256k1_scalar_clear(&gnb);
}
```

Mmh, more gibberish -- although the main idea of this implementation is actually pretty ingenious (provided you believe the NSA as mentioned above): So, the `r` and `gn` variables seem to be important, where the former looks like the current sum and `gn` is of course our secret or the number of times we're supposed to sum `r` over and over again (hence the name `ec_mult_gen`). The `gen` suffix looks like to stand for the *generator* of the Elliptic curve, which initially seems to come from the context member `ctx->initial`.

Two nice features, I like about this code is that the author tries very hard to write secure code by doing a so called "blind" multiplication, by initially adding a number `ctx->blind` to `gn`. What I find interesting, and don't really understand yet is, that this initial blind number is *not* subtracted at the end to neutralize the initial addition. I can only explain this by speculating, that either ECC multiplication is invariant w.r.t. to an initial (blind) shift or it is auto-magically taken care of implicitly within the (nested) loops. If there is somebody among my readers, who'd like to enlighten me, please drop below a comment!

The other feature I like is, that the author seems to have tried to protect the multiplication against side-channels attacks, since as we all know measuring CPU thermodynamics can reveal under the right circumstances the very secret we utilize here (see the original source on [GitHub][ecmult] with some corresponding comments, which I've omitted here for the sake of brevity).

Wow, alright! Let's re-capitulate:
```
hsk81 ~ $ bx seed | bx ec-new | bx ec-to-public
03e81a84fe1d5aa4269b0faa78110549caf3873364467688dec27c94761c2b1e6e
```

So, an initial pseudo-random *seed*, which is calculated based on the clock (according to the current implementation), is turned into a *private* key (based on HD wallets -- to be discussed in a later post), which is then morphed into a *public* key from which we can derive then an address.

**Summarized:** (*a*) measure the current time really really well (to a high degree of precision), while making sure nobody is watching; (*b*) do some *deterministic* magic to it and label it as your *private* key (and trust all your wealth upon this calculation -- including your wife and children); (*c*) then take some *publicly* available number (the initial generator of an Elliptic curve), and (*d*) multiply your *private* key with that number (again trust your wife and children upon this multiplication), deriving finally (*e*) the *public* key. Ultimately (*f*) turn this *public* key into a Bitcoin *address*.

If it were only for the initial steps (*a*) till (*e*), I would be very suspicious of this whole construction; although admittedly, it's pretty much the current state of the art in today's --
 publicly available -- cryptography.

But the last step (*f*) does mitigate a lot of the risks I see here, which I'm going to discuss in my next post.

[ECMUL]: https://3.bp.blogspot.com/-K2EV4FxZ7Eg/WPop87uTJhI/AAAAAAAAAlk/9OeHzWwwHiQy7pgrS7Sip7YI8nxetaXfgCLcB/s320/ecc_illustrated.png
[NNT]: https://www.amazon.com/Bed-Procrustes-Philosophical-Practical-Aphorisms/dp/1400069971
[ECC]: https://en.wikipedia.org/wiki/Elliptic_curve_cryptography
[evoskuil]: https://github.com/evoskuil
[ecmult]: https://github.com/bitcoin-core/secp256k1/blob/06aeea555e3580e395487a9504721c8a6f7f74a4/src/ecmult_gen_impl.h#L124