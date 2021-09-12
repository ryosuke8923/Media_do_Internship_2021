//変数
let u = 'Hello World!';

//定数
const b = 'He.. World!';

//配列
const i = [1,2,3,4,5];

//関数
const test = (arg) => {
    //ここに実行したい命令を書く
    if(i.length > arg){
        console.log('test1');
    } else {
        console.log('test2');
    }
};

document.getElementsByTagName('button')[0].addEventListener('click', () => {
    // 命令を書く
    test(3);
    window.alert('Hello World!');
});