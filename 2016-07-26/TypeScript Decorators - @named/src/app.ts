import {named} from "./named";

@named('App')
class App {
    public toString():string {
        return this['_named'];
    }

    public static toString():string {
        return App['_named'];
    }
}

let app = new App();
console.log('app.toString:', app.toString());
console.log('App.toString:', App.toString());
