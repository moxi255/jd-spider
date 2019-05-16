function search(page, page_size=5){
    var q = $('input').val()
    console.log(q)
    if (q==''){
        alert('搜索内容不能为空!')
    }
    else {
       $('a').attr({
        'style': '#'
        }) 
        var list_url = 'http://127.0.0.1:8000/api/v1/computer/search/?q='+ q +'&page=' + page +'&page_size=' + page_size;
        $.get(list_url, function(data){
            if (data['status'] && data['error'] === 0){
                $('main').empty();
                var current_page_data = data["current_page_data"];
                for (var i=0; i<current_page_data.length; i++){
                    $('main').append($('<hr>'))
                    computer= current_page_data[i];
                    var good_rate = computer.good_rate*100;
                    if (good_rate===0){
                        good_rate = '评论过少'
                    }else {
                        good_rate = good_rate.toFixed(2)+ '%'
                    }
                    div = $('<div>');
                    div.attr({
                        'style': 'display: flex; justify-content: space-between;cursor:pointer',
                        "onclick": "window.open("+ "'"+ "detail.html?computer_id=" + computer.computer_id +"')"
                    })
                    div.append($('<img>').attr({
                        'src': computer.img_url,
                        'width': 80,
                        'height': 80,
                    })).append($('<span>').text(computer.title).attr({
                        'class': 'span' + i,
                        'style': 'display:block; line-height: 80px; text-align: center; ',
                    }))
                    div.append($('<a>').attr(
                        {
                            'style': 'width:15px'
                        }
                    ))
                    div.append($('<span>').text(good_rate).attr({
                        'style': "display:block; line-height: 80px;text-align: center; color: red; font-size:18px"

                    })).append($('<a>').attr(
                        {
                            'style': 'width:15px'
                        }
                    )).append($('<sapn>').text('¥'+ computer.price).attr({
                        'style': 'color: red; font-size:20px; line-height: 80px;text-align: center; ',
                    }))
                    // 将这divt添加到main中
                    $('main').append(div)
                    $('.span'+ i).html(function (i, oldHTML) {
                    return oldHTML.replace(q, '<font color="#daa520">'+ q +'</font>')
                })
                }
                $('main').append('<br>');
                //分页部分
                //先清空nav所有内容
                $('nav').empty();
                nav = $('nav');
                nav.attr({
                    "aria-label":"Page navigation",
                    "style": "text-align: center"
                })
                ul = $('<ul>')
                ul.attr({
                    'class': "pagination"
                })
             //   判断是否有上一页
                if (data["if_has_pre_page"]){
                    ul.append($('<li>').append($('<a>').attr({
                        'href': 'javascript:search(' + (page-1) + ')',
                        'aria-label':"Previous",
                    }).append($('<span>').attr({
                        'aria-hidden':"true",
                    }).text('<上一页'))))
                }
             //   中间页部分
                for (var index in data['page_numbers']){
                    var li = $('<li>');
                    if (page===data['page_numbers'][index]){
                        li.attr({
                            'class': 'active',
                        })
                    }
                    li.append($('<a>').attr(
                        {
                            'href': 'javascript:search('+ data['page_numbers'][index] + ');',
                        }
                    ).text(data['page_numbers'][index]))
                    ul.append(li);
                }

             //   判断是否有下一页
                if (data["if_has_next_page"]){
                    ul.append($('<li>').append($('<a>').attr({
                        'href': 'javascript:' + 'search('+ (page+1) + ')',
                        'aria-label':"Next",
                    }).append($('<span>').attr({
                        'aria-hidden':"true",
                    }).text('下一页>'))))
                }
                nav.append(ul)
                if (current_page_data.length==0){
                    alert('未找到相应商品')
                }
            }else {
                alert(data['error'])
            }
        })
    }
}

function loadlist(brand, page=1, page_size=5) {
    $('a').attr({
        'style': '#'
    })
    var active_id = "'#"+ brand + "'";
    console.log(active_id)
    $('#' + brand).attr({
        'style': 'color: red'
    })
    var list_url = 'http://127.0.0.1:8000/api/v1/computer/list/?brand='+ brand +'&page=' + page +'&page_size=' + page_size;
	$.get(list_url, function(data){
		if (data['status'] && data['error'] === 0){
			$('main').empty();
			var current_page_data = data["current_page_data"];
			for (var i=0; i<current_page_data.length; i++){
			    $('main').append($('<hr>'))
                computer= current_page_data[i];
                var good_rate = computer.good_rate*100;
                if (good_rate===0){
                    good_rate = '评论过少'
                }else {
                    good_rate = good_rate.toFixed(2)+ '%'
                }
                div = $('<div>');
				div.attr({
                    'style': 'display: flex; justify-content: space-between;cursor:pointer',
                    "onclick": "window.open("+ "'"+ "detail.html?computer_id=" + computer.computer_id +"')"
				})
                div.append($('<img>').attr({
                    'src': computer.img_url,
                    'width': 80,
                    'height': 80,
                })).append($('<span>').text(computer.title).attr({
                    'style': 'display:block; line-height: 80px; text-align: center; ',
                }))
                div.append($('<a>').attr(
                    {
                        'style': 'width:15px'
                    }
                ))
                div.append($('<span>').text(good_rate).attr({
                    'style': "display:block; line-height: 80px;text-align: center; color: red; font-size:18px"

                })).append($('<a>').attr(
                    {
                        'style': 'width:15px'
                    }
                )).append($('<sapn>').text('¥'+ computer.price).attr({
                    'style': 'color: red; font-size:20px; line-height: 80px;text-align: center; ',
                }))
                // 将这divt添加到main中
                $('main').append(div)
			}
			$('main').append('<br>');
            //分页部分
			//先清空nav所有内容
            $('nav').empty();
            nav = $('nav');
            nav.attr({
                "aria-label":"Page navigation",
                "style": "text-align: center"
            })
            ul = $('<ul>')
            ul.attr({
                'class': "pagination"
            })
         //   判断是否有上一页
            if (data["if_has_pre_page"]){
                ul.append($('<li>').append($('<a>').attr({
                    'href': 'javascript:loadlist("' + brand + '",' +  (page-1) + ')',
                    'aria-label':"Previous",
                }).append($('<span>').attr({
                    'aria-hidden':"true",
                }).text('<上一页'))))
            }
         //   中间页部分
            for (var index in data['page_numbers']){
                var li = $('<li>');
                if (page===data['page_numbers'][index]){
                    li.attr({
                        'class': 'active',
                    })
                }
                li.append($('<a>').attr(
                    {
                        'href': 'javascript:loadlist("'+ brand + '",' + data['page_numbers'][index] + ');',
                    }
                ).text(data['page_numbers'][index]))
                ul.append(li);
            }
         //   判断是否有下一页
            if (data["if_has_next_page"]){
                ul.append($('<li>').append($('<a>').attr({
                    'href': 'javascript:' + 'loadlist("' + brand +'",'+ (page+1) + ')',
                    'aria-label':"Next",
                }).append($('<span>').attr({
                    'aria-hidden':"true",
                }).text('下一页>'))))
            }
            nav.append(ul)
		}else {
            alert(data['error'])
        }
	})
}
loadlist('huawei');

