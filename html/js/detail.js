function get_computer_id() {
    var loc = location.href;//获取整个跳转地址内容，其实就是你传过来的整个地址字符串console.log("我的地址"+loc);
    var n1 = loc.length;//地址的总长
    var n2 = loc.indexOf("?");//取得=号的位置
    var parameter = decodeURI(loc.substr(n2+1, n1-n2));//截取从?号后面的内容,也就是参数列表，因为传过来的路径是加了码的，所以要解码
    var parameters  = parameter.split("&");//从&处拆分，返回字符串数组
    var paValue = new Array();//创建一个用于保存具体值得数组
    for (var i = 0; i < parameters.length; i++) {
        var m1 = parameters[i].length;//获得每个键值对的长度
        var m2 = parameters[i].indexOf("=");//获得每个键值对=号的位置
        var value = parameters[i].substr(m2+1, m1-m2);//获取每个键值对=号后面具体的值
        paValue[i] = value;
    }
    return paValue[0]
}


function loaddetail(computer_id) {
    var detail_url = 'http://127.0.0.1:8000/api/v1/computer/detail/?computer_id=' + computer_id
	$.get(detail_url, function (data) {
        if (data.computer) {
            var computer = data.computer;
            var good_rate = computer.good_rate * 100;
            if (good_rate === 0) {
                good_rate = '评论过少'
            } else {
                good_rate = good_rate.toFixed(2) + '%'
            }
            $('header').append($('<h3>').text(computer.title).attr({
                'class': 'text-center text-success',
            }))
            $('main').append($('<div>').attr({
                'id': 'goods',
                'style': 'display:flex; flex-direction:row; '
            }).append($('<img>').attr({
                'src': computer.img_url,
                'width': 300,
                'height': 300,
            })).append($('<div>').append($('<dl>').attr({
                'class': 'self-dl'
            }).append($('<dt>').text('参考价:')).append($('<dd>').text('￥' + computer.price)))
                .append($('<dl>').attr({'class': 'self-dl'}).append($('<dt>').text('评论积极情感比重:')).append($('<dd>').text(good_rate)))))
            if (data.wordcloud) {
                $('main').append($('<hr>'))
                $('main').append($('<div>').attr({
                    'id': 'wordcloud'
                }).append($('<img>').attr({
                    'src': data.wordcloud
                })))
            }
            if (data.pie) {
                $('main').append($('<hr>'))
                $('main').append($('<div>').attr({
                    'class': 'svg'
                }).append($('<iframe>').attr({
                    'src': data.pie,
                    'width': 700,
                    'height': 700,
                })))
            }
            if (data.bar) {
                $('main').append($('<hr>'))
                $('main').append($('<div>').attr({
                    'class': 'svg'
                }).append($('<iframe>').attr({
                    'class': 'svg',
                    'src': data.bar,
                    'width': 700,
                    'height': 700,
                })))
            }
            if (data.top10_bar) {
                $('main').append($('<hr>'))
                $('main').append($('<div>').attr({
                    'class': 'svg'
                }).append($('<iframe>').attr({
                    'class': 'svg',
                    'src': data.top10_bar,
                    'width': 700,
                    'height': 700,
                })))
            }
            $('#param').html(computer.param)
        }else {
            alert('该商品不存在！')
            window.close()
        }
     })
}

var computer_id = get_computer_id()
loaddetail(computer_id)
