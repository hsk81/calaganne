# Libbitcoin: bx ec-to-address

Today, I'd like to discuss how you can derive a Bitcoin address from a public key using `bx ec-to-address`:

```
hsk81 ~ $ bx help ec-to-address

Usage: bx ec-to-address [-h] [--config value] [--version value]          
                        [EC_PUBLIC_KEY]

Info: Convert an EC public key to a payment address.                     

Options (named):

-c [--config]        The path to the configuration settings file.        
-h [--help]          Get a description and instructions for this command.
-v [--version]       The desired payment address version.                

Arguments (positional):

EC_PUBLIC_KEY        The Base16 EC public key to convert. If not         
                     specified the key is read from STDIN.               
```

Alright, apparently this command eats a public key, and produces an output, which we call then a Bitcoin address. Here is a way to produce one:
```
hsk81 ~ $ bx seed | bx ec-new | bx ec-to-public | bx ec-to-address
1CDR8xyAJ4vzAHoTBbXy1J14B8QhjZ366r
```

So, the `1CDR8xyAJ4vzAHoTBbXy1J14B8QhjZ366r` is a bitcoin address, which you can use to ask people to send you Bitcoins to. But beware! If you create your address this way, you omit to save your private key, and hence you would have zero possibility to spend you coins again. That would be bad. Hence, let's do this:
```
hsk81 ~ $ EC_PRIVATE=$(bx seed | bx ec-new)
hsk81 ~ $ echo $EC_PRIVATE 
fa86579eb7754d0ba98c96d0d180da7c10f1b9def22db603925b76fa9e8ec87c
```
```
hsk81 ~ $ EC_ADDRESS=$(echo $EC_PRIVATE | bx ec-to-public | bx ec-to-address)
hsk81 ~ $ echo $EC_ADDRESS
19vLj79rrErRK6q2GAcfYxRmWyT41MXcV
```

Now, we capture the private key in `EC_PRIVATE` and the address in `EC_ADDRESS`. Alright! But how does `bx ec-to-address` work under the hood?

Let's examine the source code:
```cpp
console_result ec_to_address::invoke(std::ostream& output, std::ostream& error)
{
    const auto& point = get_ec_public_key_argument();
    const auto version = get_version_option();

    output << payment_address(point, version) << std::endl;
    return console_result::okay;
}
```

Good: So, the `point` argument seems to be the public key we provide via the CLI, and the `version` is some additional argument we don't want to care about (in this post).

Then `point` is forwarded to `payment_address`, where the result is then serialized to the `output`. Good! But what does `payment_address` do? Let's check:
```cpp
payment_address::payment_address(const ec_public& point, uint8_t version)
  : payment_address(from_public(point, version))
{
}
```

Above, the constructor is just putting together the payment address with the help of the (static) `payment_address` function:
```cpp
payment_address payment_address::from_public(const ec_public& point,
    uint8_t version)
{
    if (!point)
        return payment_address();

    data_chunk data;
    return point.to_data(data) ?
        payment_address(bitcoin_short_hash(data), version) :
        payment_address();
}
```

Alright, this looks very promising: So the public key `point` is converted to some `data` chunk, hashed and then turned into a payment address. Let's have a look at that `bitcoin_short_hash`:
```cpp
short_hash bitcoin_short_hash(data_slice data)
{
    return ripemd160_hash(sha256_hash(data));
}
```

OK, so here we got the famous double hash where a `sha256` hash is re-hashed using a `ripemd160` hash! So, this is pretty much it: The result get's saved in the internal data structures of the payment address and then the whole thing is serialized using `base58` encoding:
```cpp
std::string payment_address::encoded() const
{
    return encode_base58(wrap(version_, hash_));
}
```

Finally, we've managed to work through the generation of a seed with `bx seed`, converted it into a private address with `bx ec-new`, and turned that one into a public address with `bx ec-to-public`, which was then turned into a Bitcoin address with `bx ec-to-address`.