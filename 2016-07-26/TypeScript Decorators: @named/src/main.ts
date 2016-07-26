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

var app = new App();
console.log('app.toString:', app.toString());
console.log('App.toString:', App.toString());
