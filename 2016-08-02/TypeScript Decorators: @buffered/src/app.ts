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
