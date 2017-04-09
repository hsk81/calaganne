# [Libbitcoin][1]: `bx seed`

Today, I would like to write about a project I've been following for some time now, but had simply not the capacity to devote more attention to it: [libbitcoin.org][1], which is a

> C++ Bitcoin toolkit library for asynchronous apps.

As far as I'm informed, it was originally conceived by the now (in)famous [Amir Taaki][2] with the intention to provide an alternate implementation to [Bitcoin Core][2].

When I've checked the source code on GitHub.com/libbitcoin I was simply blown away: An extremely well written piece of software, which splits the various required functionalities -- to make Bitcoin work -- into cleanly separated commands, adhering to the Unix philosophy of doing a single thing and doing it right!

Upon further investigation, I realized that an huge amount of work has been performed by [Eric Voskuil][4]: Based on my own research, it seems like that he took Amir's ingenious work and turned it into a nice piece of well organized software!

Alright, enough of talking about people. Now, let's get down to business: The point of this article is to start a series of posts about each individual command which have been implemented using [libbitcoin][5] in general and [libbitcoin-explorer][6] in particular, where the latter provides the `bx` binary, which in turn allows to access the various commands. Here is a list of them:

```bash
hsk81 ~ $ bx help

Usage: bx COMMAND [--help]

Version: 4.0.0

Info: The bx commands are:

address-decode
address-embed
address-encode
base16-decode
base16-encode
base58-decode
base58-encode
base58check-decode
base58check-encode
base64-decode
base64-encode
bitcoin160
bitcoin256
btc-to-satoshi
cert-new
cert-public
ec-add
ec-add-secrets
ec-multiply
ec-multiply-secrets
ec-new
ec-to-address
ec-to-ek
ec-to-public
ec-to-wif
ek-address
ek-new
ek-public
ek-public-to-address
ek-public-to-ec
ek-to-address
ek-to-ec
fetch-balance
fetch-header
fetch-height
fetch-history
fetch-public-key
fetch-stealth
fetch-tx
fetch-tx-index
fetch-utxo
hd-new
hd-private
hd-public
hd-to-ec
hd-to-public
help
input-set
input-sign
input-validate
message-sign
message-validate
mnemonic-new
mnemonic-to-seed
qrcode
ripemd160
satoshi-to-btc
script-decode
script-encode
script-to-address
seed
send-tx
send-tx-node
send-tx-p2p
settings
sha160
sha256
sha512
stealth-decode
stealth-encode
stealth-public
stealth-secret
stealth-shared
token-new
tx-decode
tx-encode
tx-sign
uri-decode
uri-encode
validate-tx
watch-address
watch-stealth
watch-tx
wif-to-ec
wif-to-public
wrap-decode
wrap-encode

Bitcoin Explorer home page:

https://github.com/libbitcoin/libbitcoin-explorer
```

As you see there are around `80` commands, hence I've some decent amount of work about understanding, dissecting and writing about them. The very first command I'd like to talk about is `bx seed`:

```bash
hsk81 ~ $ bx help seed

Usage: bx seed [-h] [--bit_length value] [--config value]                

Info: Generate a pseudorandom seed.                                      

Options (named):

-b [--bit_length]    The length of the seed in bits. Must be divisible by
                     8 and must not be less than 128, defaults to 192.   
-c [--config]        The path to the configuration settings file.        
-h [--help]          Get a description and instructions for this command.
```

So, it generates a *pseudorandom seed*, which means it returns a random looking number of a given bit-length:

```bash
hsk81 ~ $ bx seed
a6943c12a9e7fabd8b96ad15f6b1a24a2b7fba2d434cbbba
```

Each time you run it, you *should* get something else. Let's have a deeper look into the code at [`seed.cpp`][7]:

```cpp
console_result seed::invoke(std::ostream& output, std::ostream& error)
{
    const auto bit_length = get_bit_length_option();

    if (bit_length < minimum_seed_size * byte_bits ||
        bit_length % byte_bits != 0)
    {
        error << BX_SEED_BIT_LENGTH_UNSUPPORTED << std::endl;
        return console_result::failure;
    }

    const auto seed = new_seed(bit_length);

    output << base16(seed) << std::endl;
    return console_result::okay;
}
```

So, we see that upon doing some checks, the `new_seed` function with the `bit_length` argument is invoked delivering our `seed`, which then in turn is encoded using `based16` and send to the `output`. That was the easy part! Let's dissect `new_seed` in [`utility.cpp`][8]:

```cpp
data_chunk new_seed(size_t bit_length)
{
    size_t fill_seed_size = bit_length / byte_bits;
    data_chunk seed(fill_seed_size);
    random_fill(seed);
    return seed;
}
```

Alright, so apparently `random_fill` is our work horse here, which in turn delegates to `pseudo_random_fill` in [`random.cpp`][9]:

```cpp
void pseudo_random_fill(data_chunk& chunk)
{
    std::uniform_int_distribution<uint16_t> distribution(0, max_uint8);

    for (auto& byte: chunk)
        byte = static_cast<uint8_t>(distribution(get_twister()));
}
```

Now, it's getting interesting: Apparently a uniform distribution over `uint8` is used to query the random numbers and to fill the `chunk`. The [`get_twister`][10] function seems to deliver a seed:

```cpp
static std::mt19937& get_twister()
{
    const auto deleter = [](std::mt19937* twister)
    {
        delete twister;
    };

    static boost::thread_specific_ptr<std::mt19937> twister(deleter);

    if (twister.get() == nullptr)
    {
        // Seed with high resolution clock.
        twister.reset(new std::mt19937(get_clock_seed()));
    }

    return *twister;
}
```
Ah, we are getting closer to what's really going on: Apparently a high resolution clock is used to seed the uniform distribution. The rest around it is just some technical detail w.r.t. pseudo-random number generation. And what does [`get_clock_seed`][11] do?

```cpp
static uint32_t get_clock_seed()
{
    const auto now = high_resolution_clock::now();
    return static_cast<uint32_t>(now.time_since_epoch().count());
}
```

Alright, here we have it: The current time in high resolution is the seed! So this means, we take the current time which has elapsed since about `1970` measure it really really well, use that number as a seed for a pseudo-random generator and pick multiple `uint8` numbers uniformly at random till we have our final seed of desired length.

What does that mean? Well it means, that you should rather treat your current clock as a secret, since otherwise people could guess the result of `bx seed`, which might actually be not very difficult, if your system uses the [`ntp`][12] time synchronization protocol.

But before you start jumping around and start screaming security hole, please realize that that's the *nature* of pseudo-random generators: If you enter the same seed then you **will** get the same result. 

Hence my suggestion would be to make it really hard for outsiders to determine when exactly your `bx seed` commands are invoked, which in all practicality should be the case anyway when you disallow unauthorized access to your machine.

You could also run `bx seed` in batch at some point in time un-guessable by a potential adversary and store the results securely and safely for later retrieval. But you should asses the risk of the seeds being stolen versus the risk of some all observing adversary guessing the exact time of invocation. My gut tells me that pre-calculating the seeds would actually be less secure, than asking for them on demand.

So how does `bx seed` scale? It should take about `10` times more time, if you run it `10` times in a row, hence a linear dependency:

![][13]

As you see this is indeed the case. Here is the code I used to produce the corresponding data:

```bash
hsk81 ~ $ time for i in $(seq 1) ; do bx seed > /dev/null ; done

real	0m0.013s
user	0m0.010s
sys	0m0.000s

hsk81 ~ $ time for i in $(seq 10) ; do bx seed > /dev/null ; done

real	0m0.142s
user	0m0.107s
sys	0m0.017s

hsk81 ~ $ time for i in $(seq 100) ; do bx seed > /dev/null ; done

real	0m1.225s
user	0m0.927s
sys	0m0.190s

hsk81 ~ $ time for i in $(seq 1000) ; do bx seed > /dev/null ; done

real	0m13.423s
user	0m10.227s
sys	0m1.763s

hsk81 ~ $ time for i in $(seq 10000) ; do bx seed > /dev/null ; done

real	1m53.335s
user	1m23.380s
sys	0m11.900s
```

So, we're at then end of our investigation: I hope, that I could give you a rather in depth technical view on `bx seed` and I'm looking forward to talk about `bx ec-new` in my next post.

[1]: https://libbitcoin.org/
[2]: https://en.wikipedia.org/wiki/Amir_Taaki
[3]: https://en.wikipedia.org/wiki/Bitcoin_Core
[4]: https://github.com/evoskuil
[5]: https://github.com/libbitcoin/libbitcoin
[6]: https://github.com/libbitcoin/libbitcoin-explorer
[7]: https://github.com/libbitcoin/libbitcoin-explorer/blob/v3.0.0/src/commands/seed.cpp#L31-L48
[8]: https://github.com/libbitcoin/libbitcoin-explorer/blob/master/src/utility.cpp#L75-L81
[9]: https://github.com/libbitcoin/libbitcoin/blob/master/src/utility/random.cpp#L76-L83
[10]: https://github.com/libbitcoin/libbitcoin/blob/master/src/utility/random.cpp#L44-L63
[11]: https://github.com/libbitcoin/libbitcoin/blob/master/src/utility/random.cpp#L38-L42
[12]: http://www.ntp.org/
[13]: https://2.bp.blogspot.com/-Kaos80WSfJ0/WOo7EgKQvOI/AAAAAAAAAkk/4rj-GR-Ug80uVGQUMjz6E9rxuBZxDESTACLcB/s640/bx%2Bseed.png