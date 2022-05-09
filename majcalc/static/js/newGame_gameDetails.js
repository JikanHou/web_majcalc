var bonba = -1
var round = 1
var round_cn = "东南西北";
var number_cn = "零一二三四五六七八九十";
var game_list = []

function isInteger(x){
    return Math.floor(x) === x;
}

function getReason(id){
    return document.getElementById(id).querySelector("#reason").value;
}

function getChange(id, index){
    if (!(index >= 1 && index <= 4))
        return null;
    var player = document.getElementById(id).querySelector("#player" + String(index));
    return Number(player.querySelector("input[name=tokuten]").value);
}

function getPlayerPoint(id, index){
    if (!(index >= 1 && index <= 4))
        return null;
    var player = document.getElementById(id).querySelector("#player" + String(index));
    return Number(player.querySelector("#point").innerHTML);
}

function setPlayerPoint(id, index, point){
    if (!(index >= 1 && index <= 4))
        return;
    if (!Math.floor(point) === point)
        return;
    var player = document.getElementById(id).querySelector("#player" + String(index));
    player.querySelector("#point").innerHTML = point;
}

function getKyoutaku(id){
    return Number(document.getElementById(id).querySelector("#kyoutaku").innerHTML);
}

function setKyoutaku(id, point){
    if (Math.floor(point) === point){
        document.getElementById(id).querySelector("#kyoutaku").innerHTML = point;
    }
}

function check(){
    var game = document.getElementById(game_list[game_list.length - 1]);
    //console.log(game.querySelector(".ryuukyoku").getAttribute("hidden"));
    if (!game.querySelector(".ryuukyoku").getAttribute("hidden")){ //流局
        var tenpais = game.querySelectorAll("input[value=tenpai]");
        var notens = game.querySelectorAll("input[value=noten]");
        //console.log(tenpais.length);
        for (var i = 0; i < tenpais.length; i ++){
            if (!tenpais[i].checked && !notens[i].checked){
                var name = game.querySelector("#player" + String(i + 1)).querySelector("#name").innerHTML;
                alert("请选择" + name + "听牌情况");
                return false;
            }
        }
        var id = game_list[game_list.length - 1];
        var sum = 0;
        for (var index = 1; index <= 4; index ++){
            var temp = getChange(id, index);
            sum += temp;
        }
        if (sum % 1000 != 0 || sum < -4000 || sum > 0){
            alert("总得点有些奇怪");
            return false;
        }
        return true;
    }
    else{ //胡牌
        var tsumos = game.querySelectorAll("input[value=tsumo]");
        var rons = game.querySelectorAll("input[value=ron]");
        var houcyuus = game.querySelectorAll("input[value=houcyuu]");
        var houcyuuCnt = 0, tsumoCnt = 0, ronCnt = 0;
        for (var i = 0; i < tsumos.length; i ++){
            if (tsumos[i].checked)
                tsumoCnt ++;
            if (houcyuus[i].checked)
                houcyuuCnt ++;
            if (rons[i].checked)
                ronCnt ++;
        }
        //console.log(tsumoCnt, houcyuuCnt, ronCnt);
        if (houcyuuCnt > 1){
            alert("为什么会有多于一个人放铳？");
        }
        else if (tsumoCnt > 1){
            alert("为什么会有多于一个人自摸？")
        }
        else if (tsumoCnt > 0 && ronCnt > 0){
            alert("为什么会同时有人自摸和荣和？");
        }
        else if (ronCnt > 0 && houcyuuCnt == 0){
            alert("为什么有人荣和但是没人放铳？");
        }
        else if (tsumoCnt > 0 && houcyuuCnt > 0){
            alert("为什么同时有人自摸和有人放铳？");
        }
        else if (tsumoCnt == 0 && ronCnt == 0){
            alert("无人和牌，请使用流局界面");
        }
        else{
            var id = game_list[game_list.length - 1];
            var sum = 0;
            for (var index = 1; index <= 4; index ++){
                var p = getChange(id, index);
                if (!isInteger(p) || p % 100 != 0){
                    alert("得点不合规则！");
                    return false;
                }
                sum += p;
            }
            sum -= getKyoutaku(id);
            if (sum != 0){
                alert("总得点不为0，请注意检查供托");
                return false;
            }
            return true;
        }
        return false;
    }
}

function round_end(id){
    //alert(id);
    var round = document.getElementById(id);
    var inputs = round.querySelectorAll("input");
    for (var i = 0; i < inputs.length; i ++){
        inputs[i].setAttribute("disabled", true);
    }
    var buttons = round.querySelector("#button_div");
    buttons.setAttribute("hidden", true)

}

function round_start(id){
    //console.log("round_start" + id);
    var round = document.getElementById(id);
    var inputs = round.querySelectorAll("input");
    //console.log(inputs.length);
    for (var i = 0; i < inputs.length; i ++){
        inputs[i].removeAttribute("disabled");
    }
    var buttons = round.querySelector("#button_div");
    buttons.removeAttribute("hidden")
}

function round_ryuukyoku(){
    var current_id = String(game_list[game_list.length - 1]);
    //console.log(current_id);
    var game = document.getElementById(current_id);
    var list = game.querySelectorAll(".ryuukyoku");
    for (var i = 0; i < list.length; i ++){
        list[i].removeAttribute("hidden");
    }
    list = game.querySelectorAll(".agari");
    for (var i = 0; i < list.length; i ++){
        list[i].setAttribute("hidden", true);
    }
}

function round_agari(){
    var current_id = String(game_list[game_list.length - 1]);
    var game = document.getElementById(current_id);
    var list = game.querySelectorAll(".agari");
    for (var i = 0; i < list.length; i ++){
        list[i].removeAttribute("hidden");
    }
    list = game.querySelectorAll(".ryuukyoku");
    for (var i = 0; i < list.length; i ++){
        list[i].setAttribute("hidden", true);
    }
}

function add_round(is_new){
    if (is_new){
        round = Number(round) + 1;
        var t_bonba = bonba;
        bonba = 0;
        var last = document.getElementById(game_list[game_list.length - 1]);
        if (last){
            if (!last.querySelector(".ryuukyoku").getAttribute("hidden")){
                var lastOya = Number(game_list[game_list.length - 1].split('.')[0]);
                lastOya = last.querySelector("#player" + String((lastOya - 1) % 4 + 1));
                if (lastOya.querySelector("input[value=noten]").checked){
                    bonba = t_bonba + 1;
                }
            }
        }
        if (round > 12){
            alert("最多只支持北4局");
            return;
        }
    }
    else{
        bonba = Number(bonba) + 1;
    }
    var current_id = String(round) + "." + String(bonba);
    //console.log(current_id);
    game_list.push(current_id);

    var temp = document.getElementById("template").cloneNode(true);
    temp.removeAttribute("hidden");
    temp.setAttribute("id", current_id);

    temp.querySelector("#round_title").innerHTML = round_cn[Math.floor((Number(round) - 1) / 4)] + number_cn[(Number(round) - 1) % 4 + 1] + "局" + String(bonba) + "本场";

    var confirm_button = temp.querySelector("#confirm_button");
    confirm_button.onclick = function(){
        if (!check()){
            return;
        }
        var last = document.getElementById(game_list[game_list.length - 1]);
        var flag = true;
        var rnd = Number(game_list[game_list.length - 1].split(".")[0]);
        var oya = (rnd - 1) % 4 + 1;
        var oyaPlayer = last.querySelector("#player" + String(oya));
        if (!oyaPlayer.querySelector(".agari").getAttribute("hidden")){
            if (oyaPlayer.querySelector("input[value=tsumo]").checked || oyaPlayer.querySelector("input[value=ron]").checked)
                flag = false;
            else
                flag = true;
        }
        else if (oyaPlayer.querySelector("input[value=tenpai]").checked)
            flag = false;
        else
            flag = true;
        round_end(game_list[game_list.length - 1]);
        add_round(flag);
        var p_id = game_list[game_list.length - 2];
        var n_id = game_list[game_list.length - 1];
        var delta_kyoutaku = 0;
        for (var index = 1; index <= 4; index ++){
            delta_kyoutaku += getChange(p_id, index);
            //console.log(delta_kyoutaku);
            setPlayerPoint(n_id, index, getPlayerPoint(p_id, index) + getChange(p_id, index));
        }
        setKyoutaku(n_id, getKyoutaku(p_id) - delta_kyoutaku);
    }
    var delete_button = temp.querySelector("#delete_button");
    delete_button.onclick = function(){
        if (game_list.length == 1){
            alert("至少需要保留一局游戏");
            return;
        }
        var ret = confirm("是否删除该局？该操作不可恢复！")
        if (ret){
            document.getElementById(game_list.pop()).remove();
            round = String(game_list[game_list.length - 1]).split(".")[0];
            bonba = String(game_list[game_list.length - 1]).split(".")[1];
            round_start(game_list[game_list.length - 1]);
        }
    }
    temp.querySelector("#agari_button").onclick = round_agari;
    temp.querySelector("#ryuukyoku_button").onclick = round_ryuukyoku;
    var rnd = Number(game_list[game_list.length - 1].split(".")[0]);
    var oya = (rnd - 1) % 4 + 1;
    var oyaPlayer = temp.querySelector("#player" + String(oya));
    oyaPlayer.querySelector("#name").style.color = "red";
    for (var i = 0; i < 4; i ++){
        var p = (oya + i - 1) % 4 + 1;
        temp.querySelector("#player" + String(p)).querySelector("#kaze").innerHTML = round_cn[i];
    }
    game_record = document.getElementById("game_record");
    game_record.append(temp);
}

function window_onload(){
    add_round(false);
    document.getElementById("game_end").onclick = function(){
        var ret = confirm("是否记录该对局结果？");
        if (ret && check()){
            document.getElementById(game_list[game_list.length - 1]).querySelector("#confirm_button").click();
            document.getElementById(game_list[game_list.length - 1]).setAttribute("hidden", true);
            formData = new FormData();
            var player_list = new Array();
            for (var i = 1; i <= 4; i ++){
                player_list.push(document.getElementById("player" + String(i)).querySelector("#name").innerHTML);
            }
            var game_result = new Array();
            for (var i = 0; i < game_list.length - 1; i ++){
                var round_object = new Object();
                var id = game_list[i], next_id = game_list[i + 1];
                round_object.id = id;
                var round_result = [];
                for (var index = 1; index <= 4; index ++){
                    round_result.push(getPlayerPoint(next_id, index));
                }
                round_object.round_result = round_result;
                round_object.kyoutaku = getKyoutaku(next_id);
                round_object.reason = getReason(id);
                game_result.push(round_object);
            }
            formData.append("player_list", JSON.stringify(player_list));
            formData.append("game_result", JSON.stringify(game_result));
            $.ajax({
                url: '/game_result_upload',
                type: 'POST',
                cache: false,
                data: formData,
                processData: false,
                contentType: false
            }).fail(function (res){
                console.log(res);
                alert(res.responseText);
            }).success(function (res){
                alert("上传成功");
                window.location.href = res;
            });
        }
    }
}
window.onload = window_onload;