$(document).ready(function(){
    $('#all_box span').click(function(){
        var rr=($(this).parent().children().eq(0).text())+'-'+($(this).parent().children().eq(2).text())
        if($('#pppp').val()==''){
            $('#pppp').val(rr)
        }
        else{
            $('#pppl').val(rr)
        }

    })

    $('.lufenmatch').click(function(){
        var rr=$(this).children().eq(4).text()
        var tt=$(this).children().eq(5).text()
        $('#name1').text(rr)
        $('#name2').text(tt)
        $('input[name="zhixuceID"]').val($(this).children().eq(6).text())
        $('#lufen_alertbox').show()
    })

    var hlf=$('#havelufen').text().split(',')
    var adic={}
    for(var i=0;i<hlf.length;i++){
        adic[hlf[i]]=true;

    }
    $('.lufenmatch').each(function(){

        var qo=$(this).children().eq(6).text()
        if(adic[qo]){
            $(this).css("background-color","#D1C4A5")
            $(this).css("color","#FDF6EB")
            $(this).css("box-shadow","inset 0 1px 1px 1px #B1A07D")
        }
    })


    $('#cbox1').click(function () {
        if ($(this).prop("checked")) {
            $('.xiaozu').hide();
            $('#cbox2').prop("checked", false);
            var ll=$('#clist').text().split(',').length;
            $('#zubienum').val(ll);
        } else {
            $('.xiaozu').show();
            $('#cbox2').prop("checked", true);
            $('#zubienum').val(4);
        }
        $('.zhongzi').show()
    });
    $('#cbox2').click(function () {
        if ($(this).prop("checked")) {
            $('.xiaozu').show();
            $('#cbox1').prop("checked", false);
            $('#zubienum').val(4);
        } else {
            $('.xiaozu').hide();
            $('#cbox1').prop("checked", true);
            var ll=$('#clist').text().split(',').length;
            $('#zubienum').val(ll);
        }
        $('.zhongzi').show()
    });

    $('.jifenbiao_select_btn').click(function(){
        $('input[name="zhixuceid"]').val($(this).parent().children().eq(6).text());
        $('#jifenforminfo').submit()
    });


})


function selectcontent(){
    var typecontent=$('#dulitype').val()
    var clist=[]
    if($('#player_numshow').text().search('团队')==-1){
        if(typecontent=='全部'){
            $('#all_box span').each(function(){
                $(this).parent().show()
            })
            $('#fenzuszbox').hide();
            $('#showfenzubox').hide();
            var gg=$('#all_box').children().length
            $('#player_numshow').text(typecontent+'报名人数：'+gg)
        }
        else{
            $('#fenzuszbox').show();
            $('#showfenzubox').show();
            $('#all_box span').each(function(){
                if($(this).text()==typecontent){
                    $(this).parent().show()
    //                生成clist
                    if($(this).parent().children().eq(4).text()==''){
                        pl=($(this).parent().children().eq(0).text())+'-'+($(this).parent().children().eq(2).text())
                    }
                    else{
                        pl=($(this).parent().children().eq(0).text())+'-'+($(this).parent().children().eq(2).text())+'+'+($(this).parent().children().eq(4).text())
                    }
                    clist.push(pl)

                }
                else{
                    $(this).parent().hide()
                }
            })
            $('#player_numshow').text(typecontent+'报名人数：'+clist.length)
        }
        $('#clist').text(clist)
    }
    else{
        if(typecontent=='全部'){
            $('#all_box span').each(function(){
                $(this).parent().show()
            })
            $('#fenzuszbox').hide();
            $('#showfenzubox').hide();
        }
        else{
            $('#fenzuszbox').show();
            $('#showfenzubox').show();
        }
    }

}

function type_select(ts){
//    var gametype=$("#type").val();
//    if(gametype.search('双')!=-1){
//        $("#p2n").show()
//        $("#p2id").show()
//        $("#p2n>input").val('')
//        $("#p2id>input").val('')
//    }
//    else{
//        $("#p2n").hide()
//        $("#p2id").hide()
//        $("#p2n>input").val('')
//        $("#p2id>input").val('')
        var gametype=$(ts).val();
        if(gametype.search('双')!=-1){
            $(ts).parent().children().eq(2).show()
            $(ts).parent().children().eq(3).show()
            $(ts).parent().children().eq(2).children().val('')
            $(ts).parent().children().eq(3).children().val('')
        }
        else{

            $(ts).parent().children().eq(2).hide()
            $(ts).parent().children().eq(3).hide()
            $(ts).parent().children().eq(2).children().val('')
            $(ts).parent().children().eq(3).children().val('')

        }
//
    }



//    $("input[name='gametype']").val(gametype)


'浏览器缓存会默认加载旧的js，需要清除缓存才可以加载新的js'

//function formfill(){
//    $("input[name='matchname']").val($("#mn").val())
//    $("input[name='matchtype']").val($("#mt").val())
//}


function ftofsubmit(){
    var mt_value =[];
    $('input[name="mt"]').each(function(){
        if($(this).val()!=''){
            mt_value.push($(this).val());
        }

    });
    if(mt_value.length==0){
    alert('你还没有添加比赛类型')}
    else{
    $("input[name='matchname']").val($("#mn").val())
    $("input[name='matchBMtype']").val($("#BMt").val())
    $("input[name='matchtype']").val(mt_value)
    $("#matchinfo").submit()
    }
    }

function addmt(){
    $("#addtype").before('<input type="text" name="mt"><br/>')
}


function addpeople(){
    $("#addpeo").before("<div class='box-1' ><div class='box-1-2'><div>运动员姓名<input type='text' name='player'></div><div>运动员证件号码<input type='text' name='player'></div><div style='display:none'>运动员2姓名<input type='text' name='player' value='nan'></div><div style='display:none'>运动员2证件号码<input type='text' name='player' value='nan'></div><input type='text' value='0' name='player' style='display:none'><input type='text' value=';' name='player' style='display:none'></div></div>")
}

function addngpeople(){
    var o=$('#gtype').children()
    var m=''
    for (var i=0;i<o.length;i++){
        m+=('<option>'+o.eq(i).text()+'</option>')
    }

     $("#addngpeo").parent().parent().before('<div class="box-1"><div class="box-1-2"><div>运动员姓名<input type="text" name="player"></div><div>运动员证件号码<input type="text" name="player"></div><div style="display:none">运动员2姓名<input type="text" name="player"></div><div style="display:none">运动员2证件号码<input type="text" name="player"></div><select class="type" name="player" onclick="type_select(this)">'+m+'</select><input type="text" value=";" name="player" style="display:none"></div></div>')
}

function showform(){
    var bmtype=$("#BMtype").text()
//    alert(bmtype)
    if (bmtype=='团体报名'){
        $("#group").show()
    }
    else{
        $("#nogroup").show()
    }



}

function baomingsubmit(){
    var player_value ='';
    $('*[name="player"]').each(function(){
        if($(this).val().search('-')!=-1 || $(this).val().search(',')!=-1 || $(this).val().search('|')!=-1 || $(this).val().search('+')!=-1){
            alert('不允许使用标点符号作为名字的一部分')
            return;
        }
        else{
            player_value+=(','+$(this).val());
        }
    });
//    alert(player_value)
    if(player_value.length==0){
        alert('你还没有添加运动员')
    }
    else{
        if($("#pc").val().search('-')!=-1 || $("#pc").val().search(',')!=-1 || $("#pc").val().search('|')!=-1 || $("#pc").val().search('+')!=-1){
            alert('队伍名称不允许使用标点符号')
            return;
        }
        else{
            $("input[name='company']").val($("#pc").val())
            $("input[name='contactPeople']").val($("#contp").val())
            $("input[name='contactNumber']").val($("#contn").val())
            $("input[name='playerall']").val(player_value)
            $("#playerlist").submit()
        }

    }
}


function shufflelist(p){
    var y=p
    var len = y.length;
    for (var i = 0; i < len - 1; i++) {
        var index = parseInt(Math.random() * (len - i));
        var temp = y[index];
        y[index] = y[len - i - 1];
        y[len - i - 1] = temp;
    }
    return(y)
}

function maketeam(clist,b,renshu){
    var clista=shufflelist(clist)
    var result = [];
    for(var i=0;i<b*renshu;i+=renshu){
        result.push(clista.slice(i,i+renshu));
    }
    for(var i=b*renshu;i<clista.length;i+=(renshu+1)){
        result.push(clista.slice(i,i+renshu+1));
    }
    return(result)
}

function fenzu(){
    $('#showfenzubox').show()
    if($('#dulitype').val()=='全部'){
        alert('请选择要进行分组的比赛项目！')
        return;
    }
    else{
        var zubie=parseInt($('#zubienum').val());
        var chuxian=parseInt($('#chuxiannum').val());
        var clist=$('#clist').text().split(',').sort();
//        var clist=clist.sort()

        var a=(clist.length)%zubie
        var b=zubie-a
        var renshu=Math.floor((clist.length)/zubie)
        a=null;
//        alert('1')

    //种子选手调位置，保证不会分在同一组
        var zhongzi=[]
        zhongzi.push($('#pppp').val())
        zhongzi.push($('#pppl').val())
        if(zhongzi[0]!=''&&zhongzi[1]!=''){
            if(zhongzi[0].search('-')!=-1){
                var teamname1=zhongzi[0].match(/(\S*)-/)[1]
                var teamname2=zhongzi[1].match(/(\S*)-/)[1]
                var zzlist1=[]
                var zzlist2=[]
                var zz1_exist=1
                var zz2_exist=1
                for(var i=0;i<clist.length;i++){
                    var hj=clist[i].search(teamname1)
                    var hk=clist[i].search(zhongzi[0])
                    var hl=clist[i].search(teamname2)
                    var hm=clist[i].search(zhongzi[1])
                    if(hj!=-1&&hk==-1){
                        zzlist1.unshift(clist[i])
                    }
                    else if(hj!=-1&&hk!=-1){
                        zzlist1.push(clist[i])
                        zz1_exist*=0
                    }
                    else if(hl!=-1&&hm==-1){
                        zzlist2.unshift(clist[i])
                    }
                    else if(hl!=-1&&hm!=-1){
                        zzlist2.push(clist[i])
                        zz2_exist*=0
                    }

                }
                if(zz1_exist==1||zz2_exist==1){
                    alert('种子不存在，请检查所选比赛项目是否正确')
                    alert(zzlist1)
                    return
                }


                zzlist2.reverse()
                zzlist=[]
                for(var mn=0;mn<zzlist1.length;mn++){
                    zzlist.push(zzlist1[mn])
                }
                for(var nm=0;nm<zzlist2.length;nm++){
                    zzlist.push(zzlist2[nm])
                }
    //            alert(zzlist)
                zzlist1=null;
                zzlist2=null;


                 var temp = {}; //临时数组1
                 var temparray = [];//临时数组2
                 for (var i = 0; i < zzlist.length; i++) {
                     temp[zzlist[i]] = true;

                 }
                 for (var i = 0; i < clist.length; i++) {
                     if (!temp[clist[i]]) {
                         temparray.push(clist[i])
                     }
                 }
    //             alert(temparray)

                 newclist=[]
                 for(var bn=0;bn<temparray.length;bn++){
                    newclist.push(temparray[bn])
                 }
                 for(var nb=0;nb<zzlist.length;nb++){
                    newclist.push(zzlist[nb])
                 }
                 temparray=null;
                 temp=null;
            }
            else{
                newclist=clist
            }

        }
        else{
            alert('请输入种子选手')
            return;
        }
//        alert('2')

        result=[]
        for(var i=0;i<zubie;i++){
            a=[]
            for(var u=0;u<renshu+1;u++){
                var numid=i+u*zubie
                if(numid<newclist.length){
                    a.push(newclist[numid])
                }
                else{
                    continue;
                }
            }
            result.push(a)
        }
        result=shufflelist(result)
//        alert('3')

    //调整种子选手所在组别在头部和尾部
        if(zhongzi[0]!=''){
            for(var i=0;i<result.length;i++){
                if(String(result[i]).search(zhongzi[0])!=-1){
                    result.push(result[i])
                    result.splice(i, 1)
                }
           }
            for(var i=0;i<result.length;i++){
                if(String(result[i]).search(zhongzi[1])!=-1){
                    result.unshift(result[i])
                    result.splice(i+1, 1)
                }
            }
        }
        zhongzi=null;
//        alert('4')

    //    将分组结果输出到html
        var fzQK=''
        for(var i=0;i<result.length;i++){
            var h='<p>第'+(i+1)+'组：</p>|'
            for(var u=0;u<result[i].length;u++){
                var k='<span name="playerdetail">'+result[i][u]+'</span>|'
                h+=k
            }
            fzQK+=(h+'</br>')
        }

        var n=zubie*chuxian
        var ko=Math.log(n)/Math.log(2)
        var k=Math.ceil(ko)
        var r_num=Math.pow(2,k)-n
//        alert('5')
//        alert('ggggs')
//out of memory
        if(result[0].length==1){
//            alert('gggg')
            var f=result
        }
        else{
            var o=[]
            for(var i=1;i<(zubie+1);i++){
                for(var u=1;u<(chuxian+1);u++){
                    o.push(String(i)+String(u))
                }
            }
//            var orig=$('#originalorder').text().split(',')
            var newo=[]
            for(var i=o.length-1;i>-1;i--){
                newo.push(o[i])
            }
            var f=[]
            for(var i=0;i<o.length;i=i+2){
                f.push(o[i])
                f.push(newo[i])
            }

            o=null;
            newo=null;
            }
//        alert('6')



        for(var i=1;i<(r_num+1);i++){
            if(i%2==1){
                f.splice(i,0,'轮空')
            }
            else{
                f.splice(-(i-1),0,'轮空')
            }
        }
        showcontent='</br><div id="fenzushow_box"><div id="fenzushow">'+fzQK+'</div></div></br>'+'<div >淘汰赛排序：<span id="taotaishow">'+f+"<span></div></br><div><input type='button' value='确定分组' onclick='fillexportform()'></div>"

//<input type="button" value="交叉对战" onclick="jiaocha()">&nbsp&nbsp<input type="button" value="随机对战" onclick="suiji()">&nbsp&nbsp<input type="button" value="顺序对战" onclick="shunxu()">
        $('#showfenzu').html(showcontent)
    }
}

//function jiaocha(){
//    var orig=$('#originalorder').text().split(',')
//    var newo=[]
//    for(var i=orig.length-1;i>-1;i--){
//        newo.push(orig[i])
//    }
//    var f=[]
//    for(var i=0;i<orig.length;i+2){
//        f.push(orig[i])
//        f.push(newo[i])
//    }
//    $('#taotaishow').text(f)
//}

//function suiji(){
//    var a=$('#taotaishow').text().split(',')
//    a=shufflelist(a)
//    $('#taotaishow').text(a)
//}
//
//function shunxu(){
//    var orig=$('#originalorder').text().split(',')
//    $('#taotaishow').text(orig)
//}

function fillexportform(){
    $('input[name="exp_gametype"]').val($('#dulitype').val())
    var po=$('#fenzushow').text().replace(/第\d+组/g,'')
    var poo=po.replace(/s*/g,'')
    $('input[name="exp_fenzuqk"]').val(poo)
    $('input[name="exp_taotaiqk"]').val($('#taotaishow').text())
    $('#exportForm').submit()
}
function exportthing(){
    $('#exportall').submit()
}
function golufen(){
    $('#lufenform').submit()
}

function quedingchengji(){
    var n1=$('#name1').text()
    var n2=$('#name2').text()
    if($('#bifen11').val()==''){
        $('#lufen_alertbox').hide()
    }
    else{
        $('input[name="fenshu11"]').val($('#bifen11').val())
        $('input[name="fenshu12"]').val($('#bifen12').val())
        if(($('#bifen11').val()-$('#bifen12').val())>0){
            $('input[name="shengli1"]').val(n1)
            $('input[name="shibai1"]').val(n2)
        }
        else{
            $('input[name="shengli1"]').val(n2)
            $('input[name="shibai1"]').val(n1)
        }
        $('input[name="fenshu21"]').val($('#bifen21').val())
        $('input[name="fenshu22"]').val($('#bifen22').val())
        if(($('#bifen21').val()-$('#bifen22').val())>0){
            $('input[name="shengli2"]').val(n1)
            $('input[name="shibai2"]').val(n2)
        }
        else{
            $('input[name="shengli2"]').val(n2)
            $('input[name="shibai2"]').val(n1)
        }
        if($('#bifen31').val()!=''){
            $('input[name="fenshu31"]').val($('#bifen31').val())
            $('input[name="fenshu32"]').val($('#bifen32').val())
            if(($('#bifen31').val()-$('#bifen32').val())>0){
                $('input[name="shengli3"]').val(n1)
                $('input[name="shibai3"]').val(n2)
            }
            else{
                $('input[name="shengli3"]').val(n2)
                $('input[name="shibai3"]').val(n1)
            }
        }
        else{
            $('input[name="fenshu31"]').val(-1)
            $('input[name="fenshu32"]').val(-1)
            $('input[name="shengli3"]').val(-1)
            $('input[name="shibai3"]').val(-1)
        }

        $('.lufenmatch').each(function(){
            var qo=$(this).children().eq(6).text()
            if(qo==$('input[name="zhixuceID"]').val()){
                $(this).css("background-color","#D1C4A5")
                $(this).css("color","#FDF6EB")
                $(this).css("box-shadow","inset 0 1px 1px 1px #B1A07D")
            }
        })
        $('#lufenform').submit()

        $('#bifen11').val('')
        $('#bifen12').val('')
        $('#bifen21').val('')
        $('#bifen22').val('')
        $('#bifen31').val('')
        $('#bifen32').val('')

        $('.alertbox').hide()
    }


}

function caipansubmit(){
    var a=$('#caipan_content').val()
    if(a==''||a=='王小明、李三'){
        $('#caipan_alertbox').hide()
    }
    else{
        $('input[name="caipanlist"]').val(a)
        $('#caipanform').submit()
        $('#caipan_alertbox').hide()
    }

}
function caipanbox_alert(){
    if($('#caipan_alertbox').css('display')=='none'){
        $('#caipan_alertbox').show()
    }
    else{
        $('#caipan_alertbox').hide()
    }


}

function PdfPrintDiv() {
    //隐藏不想打印的部分
    $("#ubtn").hide();
    var wid
    var hei
    var ua = window.navigator.userAgent;
    var isIE = ua.indexOf("MSIE") != -1 || ua.indexOf("Trident") != -1;
    var isIEEdge = ua.indexOf("Edge") != -1;
    var isFirefox = ua.indexOf("Firefox") != -1;
    var isOpera = window.opr != undefined;
    var isChrome = ua.indexOf("Chrome") && window.chrome;
    var isSafari = ua.indexOf("Safari") != -1 && ua.indexOf("Version") != -1;
    if(isIE) {
        wid=window.screen.width*1400/1728;
        hei=window.screen.height*950/1152;
    } else if(isIEEdge) {
        wid=window.screen.width;
        hei=window.screen.height;
    }
//    else if(isFirefox) {
//        return "Firefox";
//    } else if(isOpera) {
//        return "Opera";
//    } else if(isChrome) {
//        return "Chrome";
//    } else if(isSafari) {
//        return "Safari";
//    }
    else {
        wid=window.screen.width;
        hei=window.screen.height;
    }
    $("body").css({"width":wid,"height":hei});
    //实现打印
//    var bdhtml = window.document.body.innerHTML;
////    sprnstr = "<!--startprint-->";
//    var eprnstr = "<!--endprint-->";
////    prnhtml = bdhtml.substr(bdhtml.indexOf(sprnstr) + 17);
//    prnhtml = prnhtml.substring(0, prnhtml.indexOf(eprnstr));
//    window.document.body.innerhtml = prnhtml;
    window.print();
    //完成后不隐藏
    $("#ubtn").show()
}