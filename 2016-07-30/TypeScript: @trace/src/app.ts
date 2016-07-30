import {named} from './named';
import {trace, traceable} from './trace';

@trace
@named('App1')
class App1 {

    public method1(a:number, b:string):void {
        console.log('>', 'instance method');
    }

    public static method2(a:number, b:string):void {
        console.log('>', 'static method');
    }
}

var app1 = new App1();
app1.method1(1, 'text1');
App1.method2(2, 'text2');

@named('App2')
class App2 {
    @traceable
    public method3(a:number, b:string):void {
        console.log('>', 'instance method');
    }
    @traceable
    public static method4(a:number, b:string):void {
        console.log('>', 'static method');
    }
}

var app2 = new App2();
app2.method3(3, 'text3');
App2.method4(4, 'text4');
