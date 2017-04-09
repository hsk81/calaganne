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

