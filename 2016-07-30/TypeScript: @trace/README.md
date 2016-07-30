# TypeScript Decorators: @trace

Alright, we want to be able to trace our [TypeScript classes][1] using a simple decorator:
```typescript
@trace
class App {
    public method(n:number, text:string) {
    }
}

let app = new App();
app.method(1, 'text')
```

This shall produce the following output:
```
[2016-07-30T12:23:25.520Z]#bc0b >>> @.method
[2016-07-30T12:23:25.520Z]#bc0b { '0': 1, '1': 'text' }
[2016-07-30T12:23:25.546Z]#bc0b <<< @.method
[2016-07-30T12:23:25.546Z]#bc0b undefined
```

Above, we shall have the time stamp of the invocation followed by some random string (identifying identical invocations). Then, we shall have the method name plus, on the second line, a list of arguments. Further, on the third line, we shall have the time stamp of the return, and finally on the last line the resulting value.

By default, the method name shall not include the corresponding class name. To create fully qualified method names the `@named` decorator shall be used:
```
@trace
@named('App')
class App {/*..*/}
```

Further, we want to be able to provide a `boolean` flag to `@trace` to switch tracing on and off:

```typescript
@trace(false)
class App {/*..*/}
```

Further, we want the ability to trace a class but omit certain methods, we're not interested in (since maybe they are called simply too often and tracing the corresponding invocations would quickly become infeasible):
```
@trace
class App {
    public method1(n:number, text:string) {/*..*/}

    @traceable(false)
    public method2(n:number, text:string) {/*..*/}
}
```

We also want the opposite, where only certain methods shall be traced, while in general the rest of the class shall be left alone:
```
class App {
    public method1(n:number, text:string) {/*..*/}

    @traceable
    public method2(n:number, text:string) {/*..*/}
}
```

How do we implement all this various tracing features? Here it is:
```typescript
import './random';

export function trace(
    flag:boolean):Function;
export function trace(
    ctor:Function):void;
export function trace(
    arg0:boolean|Function):Function|void
{
    if (typeof arg0 === 'boolean') {
        return _trace(arg0);
    } else {
        _trace(true)(<Function>arg0);
    }
}

function _trace(flag:boolean):Function {
    return function (ctor:Function) {
        Object.keys(ctor.prototype).forEach((key:string) => {
            let fn:any = ctor.prototype[key];
            if (typeof fn === 'function') {
                _traceable(flag)(ctor.prototype, key);
            }
        });
        Object.keys(ctor).forEach((key:string) => {
            let fn:any = (<any>ctor)[key];
            if (typeof fn === 'function') {
                _traceable(flag)(ctor, key);
            }
        });
    }
}

export function traceable(
    flag:boolean):Function;
export function traceable(
    target:any, key:string, descriptor?:PropertyDescriptor):void;
export function traceable(
    arg0:boolean|any, key?:string, descriptor?:PropertyDescriptor
):Function|void {
    if (typeof arg0 === 'boolean') {
        return _traceable(arg0);
    } else {
        _traceable(true)(<any>arg0, key, descriptor);
    }
}

function _traceable(flag:boolean):Function {
    return function (
        target:any, key:string, descriptor?:PropertyDescriptor)
    {
        let fn:Function = descriptor ? descriptor.value : target[key];
        if (!flag) {
            (<any>fn)['_traced'] = false;
        } else {
            if ((<any>fn)['_traced'] === undefined) {
                (<any>fn)['_traced'] = true;

                let tn:Function = function () {
                    let _named = target._named || '@',
                        random = String.random(4, 16),
                        dt_beg = new Date().toISOString();

                    console.log(
                        `[${dt_beg}]#${random} >>> ${_named}.${key}`);
                    console.log(
                        `[${dt_beg}]#${random}`, arguments);

                    let result = fn.apply(this, arguments),
                        dt_end = new Date().toISOString();

                    console.log(
                        `[${dt_end}]#${random} <<< ${_named}.${key}`);
                    console.log(
                        `[${dt_end}]#${random}`, result);

                    return result;
                };
                for (let el in fn) {
                    if (fn.hasOwnProperty(el)) {
                        (<any>tn)[el] = (<any>fn)[el];
                    }
                }
                if (descriptor) {
                    descriptor.value = tn;
                } else {
                    target[key] = tn;
                }
            }
        }
    }
}

export default trace;
```

The details are onerous, but the main idea is simple: Wrap a method, which shall be traced, with a function printing the method name and arguments *before* the invocation, and the result *after* the invocation.

As hinted above, we shall be able to write `@trace` or `@trace(true|false)` (and similarly `@traceable` or `@traceable(true|false)`): In the implementation this is achieved using [function overloads][2].

A last point which is worth of mentioning is the fact, that *static* methods can be traced as well:
```
@trace
class App {
    public static method1(n:number, text:string) {/*..*/}

    @traceable(false)
    public static method2(n:number, text:string) {/*..*/}
}
```

[1]: http://www.typescriptlang.org/docs/handbook/classes.html
[2]: http://www.typescriptlang.org/docs/handbook/functions.html
