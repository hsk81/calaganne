# TypeScript Decorators: @named

I’ve been playing around recently with this fantastic new language [TypeScript][1] in general plus with [TypeScript decorators][2] in particular, and would like to share some of my experiences. In this post I’ll keep things to the bare minimum, and will elaborate more in the upcoming posts of mine.

Alright, let’s dive in: I actually wanted to build my own tracing system, where I would see which parts of my code are invoked when, with which arguments and returning with which results.

I was particularly interested in class methods: However, I figured out rather soon that the name of the class is not accessible, unless you would use [metadata reflection][3]. But since the latter seems to be rather experimental, I decided to go for my own minimal thing.

So, the easiest approach I imagined was to simply attach any name of my choice to a class of mine using decorators:

```typescript
import {named} from "./named";

@named('App')
class App {
    public toString():string {
        return this['_named'];
    }

    public static toString():string {
        return this['_named'];
    }
}

var app = new App();
console.log('app.toString:', app.toString());
console.log('App.toString:', App.toString());
```

Yes, it’s cheap but hey I was looking for a quick and working solution! So, when we run `npm start` the output should look like:

```bash
app.toString: App
App.toString: App
```

As you see, it works: Both the instance and static `toString` methods manage to return the expected `App` string. This little feature will become later important for us to provide tracing using fully qualified function names.

Let’s check the `named.ts` implementation: It’s rather straight forward, since the supplied named string is attached as the `_named` instance and static member directly to the `object`.

```typescript
export function named(name:string) {
    return function (object:any) {
        if (object.prototype._named === undefined) {
            object.prototype._named = name;
        }
        if (object._named === undefined) {
            object._named = name;
        }
    };
}

export default named;
```

The source code of this example is available on [GitHub.com][4]:
```bash
git clone git@github.com:hsk81/calaganne calaganne.git
cd 'calaganne.git/2016-07-26/TypeScript Decorators: @named'/
```

Further, you have to install the `npm` dependencies (and compile the project):
```bash
npm install
```

Now, you should be able to start the application as already mentioned above:
```bash
npm start
```

[1]: http://www.typescriptlang.org/index.html
[2]: http://www.typescriptlang.org/docs/handbook/decorators.html
[3]: http://www.typescriptlang.org/docs/handbook/decorators.html#metadata
[4]: https://github.com/hsk81/calaganne/tree/master/2016-07-26/TypeScript%20Decorators:%20%40named