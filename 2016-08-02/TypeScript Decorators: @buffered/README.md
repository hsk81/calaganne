# [TypeScript Decorators][1]: @buffered

There are many circumstances, where a developer desires to ignore subsequent invocations of a function, except the last one. For example, you may want to ignore a crazy user's high speed clicking, till he stops doing so: Only the very last click should cause an action.

But how do we define *last* in this context? Well, a simple way to do it, is to *buffer* all invocations of a function, and then invoke only the very *last* one, after which (for a certain time window) no such invocation is triggered by the manic user.

For example, I could put the buffer threshold to `200` milli-seconds: This will cause very fast clicks to be interpreted as a single click, but any two subsequent clicks, which are apart by more than `200` milli-seconds, will be interpreted as two *separate* clicks. Let's have a look at a toy example:
```typescript
import {buffered} from "./buffered";

class App {
    public nilHundredMsAgo() {
        console.log('[000-ms-ago]', new Date().toISOString());
    }
    @buffered
    public twoHundredMsAgo() {
        console.log('[200-ms-ago]', new Date().toISOString());
    }
}

let app = new App();
app.nilHundredMsAgo();
app.twoHundredMsAgo();
```

If we run the example we get:
```bash
$ npm start
[000-ms-ago] 2016-08-02T11:20:50.463Z
[200-ms-ago] 2016-08-02T11:20:50.667Z
```

As you see above their is a time difference of *at least* `200` milli-seconds, which confirms that the `App.twoHundredMsAgo` method has been successfully buffered. Let's extend the above example:
```typescript
import {buffered, IBufferedFunction} from "./buffered";

class App {
    public nilHundredMsAgo() {
        console.log('[000-ms-ago]', new Date().toISOString());
    }
    @buffered
    public twoHundredMsAgo() {
        console.log('[200-ms-ago]', new Date().toISOString());
    }
    @buffered(600)
    public sixHundredMsAgo() {
        console.log('[600-ms-ago]', new Date().toISOString());
    }
}

let app = new App();
app.nilHundredMsAgo();
app.twoHundredMsAgo();

let fn:Function = app.sixHundredMsAgo;
for (let i = 0; i<256; i++) fn();
let bn = <IBufferedFunction>fn;
bn.cancel();
```

And this time, if we run the extended example we get:
```bash
$ npm start
[000-ms-ago] 2016-08-02T11:23:59.159Z
[200-ms-ago] 2016-08-02T11:23:59.362Z
```

This looks like the previous output from before! What happened at the `256` different invocations of `App.sixHundredMsAgo`? Well, they got canceled because of which none of the invocations produced any time stamp. 

Accessing the `cancel` function is a little awkward, since the corresponding method is required first to be converted to a `Function` and then again to a `IBufferedFunction`, which has `cancel` declared. But since it is expected that cancelling a buffered method is not to be used that often, we can live with the way to access `cancel`.

Further, please also note that above we used `@buffered(600)`, to change the default time window from `200` to `600` milli-seconds. Alright, let's have a look at a final and more realistic example:
```typescript
/// <reference path="lib/jquery/index.d.ts" />
import {buffered} from './buffered';

class App {
    public constructor() {
        $('#my-button').on('click', this.onClick.bind(this));
    }

    @buffered
    public onClick(ev:MouseEvent) {
        console.log('[on:click]', ev);
    }
}

let app = new App();
```

As you see above, by simply decorating the `onClick` handler with `@buffered` we can fend off crazy users, who have lost their minds and became click-o-maniacs! Please also note, that we used [jQuery][2] to subscribe the *buffered* handler to `click` mouse events.

Finally, here is the magic that enables us to use the `@buffered` decorator:
```typescript
export interface IBufferedFunction extends Function {
    cancel:Function;
}

export function buffered(
    ms:number):Function;
export function buffered(
    target:any, key:string, descriptor?:PropertyDescriptor):void;
export function buffered(
    arg:number|any, key?:string, descriptor?:PropertyDescriptor
):Function|void {
    if (typeof arg === 'number') {
        return _buffered(arg);
    } else {
        _buffered(200)(<any>arg, key, descriptor);
    }
}

function _buffered(ms:number) {
    return function (
        target:any, key:string, descriptor?:PropertyDescriptor
    ) {
        let fn:Function = descriptor ? descriptor.value : target[key],
            id:number;
        let bn:Function = function (...args:any[]) {
            if (id !== undefined) {
                clearTimeout(id);
                id = undefined;
            }
            if (id === undefined) {
                id = setTimeout(() => {
                    fn.apply(this, args);
                    id = undefined;
                }, ms);
            }
        };
        for (let el in fn) {
            if (fn.hasOwnProperty(el)) {
                (<any>bn)[el] = (<any>fn)[el];
            }
        }
        (<IBufferedFunction>bn).cancel = function () {
            if (id !== undefined) {
                clearTimeout(id);
                id = undefined;
            }
        };
        if (descriptor) {
            descriptor.value = bn;
        } else {
            target[key] = bn;
        }
    };
}

export default buffered;
```

[1]: http://www.typescriptlang.org/docs/handbook/decorators.html
[2]: https://api.jquery.com/on/
