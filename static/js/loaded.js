//frame1
function updateCurrentTime() {
    let currentTime = new Date();
    let minutes = currentTime.getMinutes();
    let seconds = currentTime.getSeconds();

    // 计算距离下一分钟的延迟时间
    let delay = (60 - seconds) * 1000;

    // 更新当前时间
    let hours = currentTime.getHours();
    document.getElementById('current-time').innerHTML = hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0');

    // 下一分钟时执行更新操作
    setTimeout(updateCurrentTime, delay);
}

// 更新当前时间
updateCurrentTime();

// 获取当前日期
let options = {year: 'numeric', month: 'long', day: 'numeric'};
let currentDate = new Date().toLocaleDateString('zh-CN', options);

// 获取当前星期几
let currentWeekday = new Date().toLocaleDateString('zh-CN', {weekday: 'long'});

// 获取当前农历
let lunarString = Solar.fromYmd(new Date().getFullYear(), new Date().getMonth() + 1, new Date().getDate()).getLunar();

// 显示当前日期、星期几和农历
document.getElementById('current-date').innerHTML = currentDate + " " + currentWeekday;
document.getElementById('current-lunar').innerHTML = lunarString;
//frame2
let todayHighestTemp = parseInt(document.getElementById("today-highest-temp").textContent.replace("℃", ""));
let todayLowestTemp = parseInt(document.getElementById("today-lowest-temp").textContent.replace("℃", ""));
let temperatureBar = document.getElementById("temperature-bar");
//第一版方案
const switchVersion = 2;
let zoom,zoomValue,offsetValue;
if (switchVersion === 1) {
    zoom = 200/500 * (100 / (todayHighestTemp - todayLowestTemp));
    zoomValue = 500/200 * 100 * zoom;
    offsetValue = -(50 - todayHighestTemp) * 5 * zoom;
}
if (switchVersion === 2) {
    zoom = 200/500 * (100 / (todayHighestTemp - todayLowestTemp)) / 2;
    zoomValue = 500/200 * 100 * zoom;
    // offsetValue = -(50 - todayHighestTemp - (todayHighestTemp - (todayHighestTemp + todayLowestTemp) / 2)) * 5 * zoom;
    offsetValue = 500*zoom*((todayLowestTemp-50)/100);
    console.log("offsetValue:",offsetValue)
    console.log("zoom:",zoom)
}
    temperatureBar.style.backgroundSize = "auto " + zoomValue + "%";
    temperatureBar.style.backgroundPosition = "center bottom " + offsetValue + "px";



//frame3
function editNodeHeight(textClassName, nodeClassName, barType) {
    let baseHeight;
    let texts = document.getElementsByClassName(textClassName);//获取文字class
    let nodes = document.getElementsByClassName(nodeClassName);//获取nodeClass
    let containArr = Array.from({length: nodes.length}, () => ({}));//创建数组

    for (let [index, obj] of containArr.entries()) {//数组赋值
        obj.element = nodes[index];
        obj.floatText = parseFloat(texts[index].textContent.replace(/[℃m]/g, ""));
        obj.rank = 0;
        obj.height = 0;
    }

    containArr.sort((a, b) => {
        // 按照 HeightValue 属性的值从小到大排序
        return a.floatText - b.floatText;
    });

    // 设置相应的 rank 值为排序的名次
    let rank = 1;
    for (let i = 0; i < containArr.length; i++) {
        // 当前元素的 HeightValue 与前一个元素不同时，更新名次
        if (i > 0 && containArr[i].floatText !== containArr[i - 1].floatText) {
            rank++;
        }
        // 设置 rank 值为名次
        containArr[i].rank = rank;
    }
    let rankMax = rank;
    if (barType === "precip") {
        baseHeight = 0;
    } else {
        baseHeight = 20;
    }
    for (let i = 0; i < containArr.length; i++) {
        if (rankMax === 1) {
            containArr[i].height = baseHeight;
        } else {
            containArr[i].height = baseHeight + 70 / (rankMax - 1) * (containArr[i].rank - 1);

        }
        containArr[i].element.style.height = containArr[i].height + "px";
    }

    return null;
}

editNodeHeight("temp-text", "temp-node", "temp");//按温度修改温度条高度
editNodeHeight("precip-text", "precip-node", "precip");//按降水修改降水条高度

let tempNode = document.getElementsByClassName("temp-node");
// let tempText = document.getElementsByClassName("temp-text");
// let precipNode = document.getElementsByClassName("precip-node");
// let precipText = document.getElementsByClassName("precip-text");
//let weatherForecastInfo = [];
let zoomTini,zoomVaLueTini,offsetValueTini;
for (let i = 0; i <= 6; i++) {
    // weatherForecastInfo[i] = {
    //     "tempNodeHeight": tempNode[i].getBoundingClientRect().height,
    //     "tempTextContent": parseInt(tempText[i].textContent.replace("℃", "")),
    //     "precipNodeHeight": precipNode[i].getBoundingClientRect().height,
    //     "precipTextContent": parseInt(precipText[i].textContent.replace("m", ""))
    // let zoomValueTini = (200 * zoomValue) / (tempNode[i].getBoundingClientRect().height)/2.222;
    let zoomValueTini = zoomValue * 90 / (tempNode[i].getBoundingClientRect().height);
    tempNode[i].style.backgroundSize = "auto " + zoomValueTini + "%";
    console.log((90-tempNode[i].getBoundingClientRect().height)+ "px");
    tempNode[i].style.backgroundPosition = "center bottom " +offsetValue/2.222+"px";
}

function getHoursArr(cHour) {
    let hoursArr = [cHour + 1, cHour + 3, cHour + 5, cHour + 7, cHour + 9, cHour + 11, cHour + 13];
    return hoursArr.map(function (value) {
        // 如果元素大于 24，则减去 24
        if (value >= 24) {
            return value - 24;
        }
        // 否则保持不变
        return value;
    });

}

let currentHourArr = getHoursArr(new Date().getHours());
//获取当前整点时间
document.getElementById('1-hours-later').innerHTML = currentHourArr[0] + ":00";
document.getElementById('3-hours-later').innerHTML = currentHourArr[1] + ":00";
document.getElementById('5-hours-later').innerHTML = currentHourArr[2] + ":00";
document.getElementById('7-hours-later').innerHTML = currentHourArr[3] + ":00";
document.getElementById('9-hours-later').innerHTML = currentHourArr[4] + ":00";
document.getElementById('11-hours-later').innerHTML = currentHourArr[5] + ":00";
document.getElementById('13-hours-later').innerHTML = currentHourArr[6] + ":00";
//整体
let backgroundStyle = document.getElementById('background').style;
if (!backgroundStyle.backgroundImage) {
    backgroundStyle.backgroundColor = 'black';
}
