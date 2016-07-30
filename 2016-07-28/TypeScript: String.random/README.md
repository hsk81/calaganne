# TypeScript: String.random

Today, I'd like to discuss and analyze a function I'm using quite often during my daily work with [TypeScript][1]. It's about generating random strings, and here is the code:

```typescript
interface StringConstructor {
    random(length?:number, range?:number):string;
}

String.random = function (length:number, range:number = 36):string {

    length = Math.floor(length);
    range = Math.floor(range);

    let p_0 = Math.pow(range, length),
        p_1 = range * p_0;

    return (length > 0) 
        ? Math.floor(p_1 - p_0 * Math.random()).toString(range).slice(1)
        : '';
};
```

So, I attach the `random` function to the `String` interface: Yes, normative pundits will point out now that I should not overwrite or extend any existing vanilla constructions, but since I use random strings so often, I decided to commit this sin in the name of convenience!

Further, since the result of `random` is a string, there was no better place for me than to attach the former to the latter. If you cannot follow my logic, so be my guest and put the function where ever you deem it best.

Alright, after having addressed the dogmatic computer scientists, it's time to have a look how we use `String.random`:

```typescript
import './random';

let random_1 = String.random(8);
console.log(`random-1 w/{length:8, range:36}: ${random_1}`);
let random_2 = String.random(6, 16);
console.log(`random-2 w/{length:6, range:16}: ${random_2}`);
let random_3 = String.random(4, 2);
console.log(`random-3 w/{length:4, range: 2}: ${random_3}`);
```

The above code produces on the terminal the following random strings:
```bash
random-1 w/{length:8, range:36}: bicgtcoq
random-2 w/{length:6, range:16}: 8cf784
random-3 w/{length:4, range: 2}: 0110
```

So, apparently the `length` argument controls the number of characters in the random strings, while the `range` argument sets the range of characters from which they are chosen from. Do *not* put a range larger than `36`, since otherwise the `number.toString(range)` function, which is used to convert numbers to strings, will complain very loudly!

## PRNGs and Uniform Distributions

Well, so far for the practical side of the code; let's investigate the theoretical side of randomness: Computers cannot create "true" random numbers, but rely on so called [pseudo-random generators][2] (PRNG). In our case, we rely on `Math.random()` to deliver a reasonably usable (discrete) [uniform distribution][3]. The latter reference describes it as:

> In probability theory and statistics, the discrete uniform distribution is a symmetric probability distribution whereby a finite number of values are equally likely to be observed; every one of $n$ values has equal probability $1/n$.

Or using a simpler language:

> Another way of saying "discrete uniform distribution" would be "a known, finite number of outcomes equally likely to happen".

Actually, getting randomness is in general quite hard and it's a science: So, do *not* try to use in security related applications your homegrown PRNGs, but rely on well researched algorithms and correct implementations!

In this context, I'd recommend to even forgo the above code and use for example the [Stanford Javascript Crypto Library][4]. However, if you need some quick and good enough implementation then `String.random` might be your candidate.

## Analysis of the Distribution

So what is good enough? Well, the distribution of the random strings should be uniform. Let's produce the data to analyze, where we'll generate binary random strings with a length of $16$ characters:

```typescript
import './random';

class App {
    public logRandom(size:number) {
        for (let i=0; i<size; i++) {
            console.log(String.random(16, 2))
        }
    }
}

let app = new App();
app.logRandom(65536);
```

This will create a huge list of binary random strings: But how do we determine if it is *uniform*? Creating directly a [histogram][5] might be an approach, but we might not have enough data to gain significant insight.

Why is that? The total number of binary strings of size $16$ --- which is $2^{16}=65536$ --- happens to be the number of samples we have in our data. So we would expect to see each binary string on average only *once*: Counting each string once, and creating a corresponding histogram might confirm that we might not have a very skewed distribution, but that's pretty much it.

However, for uniformly distributed binary strings the following property should hold as well: *The number of different characters between any two strings should follow a [normal distribution][6]*. Let's check this with a small Python script:

```python
#!/usr/bin/env python

from matplotlib import pyplot as pp
import numpy as np
import sys

def levenstein(source, target):
    if len(source) < len(target):
        return levenstein(target, source)
    if len(target) == 0:
        return len(source)

    source = np.array(tuple(source))
    target = np.array(tuple(target))

    prev_row = np.arange(target.size + 1)
    for s in source:
        curr_row = prev_row + 1
        curr_row[1:] = np.minimum(
                curr_row[1:], np.add(prev_row[:-1], target != s))
        curr_row[1:] = np.minimum(
                curr_row[1:], curr_row[0:-1] + 1)
        prev_row = curr_row

    return prev_row[-1]

with open(sys.argv[1]) as file:
    lines = list(map(lambda l: l[:-1], file.readlines()))

ds, l0 = [], lines[0]
for line in lines[1:]:
    d = levenstein(line, l0)
    if d > 0: ds.append(d)

pp.title('Levenstein Differences')
pp.hist(ds, bins=13)
pp.grid()
pp.show()
```

And finally let's have a look at the histogram:

![Levenstein Differences][7]

So this pretty much confirms our expectation: The histogram is symmetric around a difference of $7$ characters and fitting a normal distribution to this data should not be a problem. 

We conclude that an original uniform distribution might have caused the observed normal distribution, and will stop analyzing further. Of course many more statistical tests should be carried out to determine beyond doubt the quality of the PRNG, but will stop here for the sake of brevity.

[1]: http://www.typescriptlang.org/index.html
[2]: https://en.wikipedia.org/wiki/Pseudorandom_number_generator
[3]: https://en.wikipedia.org/wiki/Discrete_uniform_distribution
[4]: https://github.com/bitwiseshiftleft/sjcl
[5]: https://en.wikipedia.org/wiki/Histogram
[6]: https://en.wikipedia.org/wiki/Normal_distribution
[7]: https://3.bp.blogspot.com/-hvMViBY_fMg/V5ngv183mpI/AAAAAAAAAUo/oTORaAFRlQctvriE2W---e76sUYJtth0ACLcB/s640/app.png
