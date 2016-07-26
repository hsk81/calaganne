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
