import './random';

class App {
    public logRandom(size:number) {
        for (let i=0; i<size; i++) {
            console.log(String.random(8, 16))
        }
    }
}

var app = new App();
app.logRandom(1024);
