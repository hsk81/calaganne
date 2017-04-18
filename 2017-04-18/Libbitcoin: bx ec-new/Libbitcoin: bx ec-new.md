# Libbitcoin: bx ec-new

Today, I'd like to present the `bx ec-new` command which generates a private key from entropy. For the uninitiated, *entropy* means just some random noise and a *private* key means that it allows you to *spend* your Bitcoins (by allowing you to sign corresponding transactions). And the `ec` prefix stands for [Elliptic Curves][1], which is an efficient way of implementing public key cryptography.

In public key cryptography you have a *private* and a *public* key pair, where the former is used to encrypt messages, and the latter is used to decrypt them. The key pair can also be used to sign and verify messages (or in our case, transactions).

Now, let's check what the integrated help systems of [libbitcoin's explorer][0] tells us:
```
hsk81 ~ $ bx help ec-new

Usage: bx ec-new [-h] [--config value] [SEED]                            

Info: Create a new Base16 EC private key from entropy.                   

Options (named):

-c [--config]        The path to the configuration settings file.        
-h [--help]          Get a description and instructions for this command.

Arguments (positional):

SEED                 The Base16 entropy for the new key. Must be at least
                     128 bits in length. If not specified the seed is    
                     read from STDIN.                   
```

Alright, so we apparently need some `SEED` which we need to feed to the `ec-new` monster so we get our private key (using a hexadecimal encoding). The seed can be generated for example with `bx seed` and piped through to `ec-new`:
```
hsk81 ~ $ bx seed | bx ec-new
172a430e125bbab14a76847db2344835783fc501d44893a0ed3c43e58d0712d4
```

Or if you want to avoid `bx seed` and read directly from a random source like `urandom` (available on Linux systems) you could also just do this:
```
hsk81 ~ $ head -c 1024 /dev/urandom | tr -dc '0-9a-f' | fold -w 48 | head -n 1 | bx ec-new
a9d0daf848e00825bbe3f2cf3a85b4316ccbe15d6207567b215e92b238de4def
```

Yes, it's more tedious, but there is *no dependency* on the system clock like in the case of `bx seed`. But when you would ask me, which one is more secure, answering that would be beyond me to judge, since `bx seed` does some fancy twisting to the system clock, which is then fed to a uniform pseudo-random generator. However, `urandom` is also not be underestimated either, since it collects according to its manual page entropy from *various* parts of the operating system, to deliver useful randomness. I guess querying both a few billion times and running fancy statistical tests to measure their entropy would be a nice exercise for the interested reader.

But let's focus on `ec-new`: As mentioned, it's based on [Elliptic Curves][1] and uses according to the source code a `new_key(seed)` invocation to derive a secret from the given `seed`:

```cpp
console_result ec_new::invoke(std::ostream& output, std::ostream& error)
{
    const data_chunk& seed = get_seed_argument();
    if (seed.size() < minimum_seed_size)
    {
        error << BX_EC_NEW_SHORT_SEED << std::endl;
        return console_result::failure;
    }

    ec_secret secret(new_key(seed));
    if (secret == null_hash)
    {
        error << BX_EC_NEW_INVALID_KEY << std::endl;
        return console_result::failure;
    }

    output << config::ec_private(secret) << std::endl;
    return console_result::okay;
}
```

The `new_key` function is based on [BIP32][2], which describes so called *hierarchical deterministic wallets*  (or *HD Wallets*): Basically a fancy way to derive multiple public and private keys based on a master key. I'll defer a deeper look into these HD wallets to a later post, since there are specific `bx` commands which deal directly with them:

```cpp
ec_secret new_key(const data_chunk& seed)
{
    const wallet::hd_private key(seed);
    return key.secret();
}
```

So, that's it for today. I keep this post short, since it's getting rather late, although there is so much to write about this little `bx ec-new` command: It's in my opinion, pretty much the foundation stone (or one of them) upon which Bitcoin is built, producing a private key to keep your coins safe and spend them at will.

But for the complete uninitiated, I will offer a rather not so perfect analogy: You could compare `bx ec-new` to a bank employee creating an account for you (after asking you to come up with some random number), and then handing you a secret for the created account. This secret will allow you to access and transfer your funds. The nice part here is that there is neither a bank, nor an employee but just you and your computer (or smart phone) performing all the magic.

[0]: https://libbitcoin.org/

[1]: https://en.wikipedia.org/wiki/Elliptic_curve_cryptography

[2]: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki