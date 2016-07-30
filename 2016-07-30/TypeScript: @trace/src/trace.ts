import './random';

export function trace(
    ctor:Function
) {
    Object.keys(ctor.prototype).forEach((key:string) => {
        let fn:any = ctor.prototype[key];
        if (typeof fn === 'function') {
            traceable(ctor.prototype, key);
        }
    });
    Object.keys(ctor).forEach((key:string) => {
        let fn:any = (<any>ctor)[key];
        if (typeof fn === 'function') {
            traceable(ctor, key);
        }
    });
}

export function traceable(
    target:any, key:string, descriptor?:PropertyDescriptor
) {
    let fn:Function = descriptor ? descriptor.value : target[key];
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

export default trace;
