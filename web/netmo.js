$(function(){
    var hostsObj  = $('#hosts');
    var linesObj = $('#lines');
    var svgObj = $('#lines svg');
    var portsObj  = $('#ports');
    var blockHeight = 34;
    var svgWidth = svgObj.width();
    var maxHosts = 10;

    var config = {
        hiliteFade: 1000,
        lineWidth : '1',
        lineFadeDelta : 0.1,
        boxFadeTime : 2000,
        messageSlideTime: 10,
        maxMessages: 10,
        lineColour: '#555'
    };

    function makeNewElement(text, parent){
        var elName  = $('<span></span>');
        var elCount = $('<span></span>');
        var elObj   = $('<div></div>');
        elObj.append(elName, elCount);
        elName.text(text);
        
        parent.append(elObj);
        elObj.setCounter = function(count){
            //elCount.text(count);
            //elObj.prependTo(parent);
        };
        elObj.setName = function(name){
            elName.text(name);
            elObj.addClass('hilite');
            setTimeout(function(){
                elObj.removeClass('hilite');
            }, config.hiliteFade);
        };
        elObj.getIndex = function(){
            return parent.find('div').index(elObj);
        };
        elObj.css('z-index', 10)
        return elObj;
    }

    function drawLine(hostIndex, portIndex){
        var path = $(document.createElementNS( "http://www.w3.org/2000/svg", 'path'));
        var startY = (hostIndex + 0.5) * blockHeight;
        var endY = (portIndex + 0.5) * blockHeight;

        path.attr('d', ['m 0,', startY, ' c 50,0 150,', (endY-startY), ' ', svgWidth, ',', (endY - startY)].join(''));
        path.attr('stroke', config.lineColour);
        path.attr('fill', 'none');
        path.attr('stroke-width', config.lineWidth);
        var opacity = 1, delta = config.lineFadeDelta;
        var interval = setInterval(function(){
            opacity -= delta;
            path.attr('stroke-opacity', opacity);
            if (opacity <= 0){
                clearInterval(interval);
                path.remove();        
            }
        },50);
        svgObj.append(path);
    }

    var hostsData = (function(){
        var obj = {}, data = {};

        obj.getHostObject = function(address){
            if (!(address in data)){
                var initialLife = 10;
                var o  = {
                    'el' : makeNewElement(address, hostsObj),
                    'count' : 0,
                    'ondata' : function(){
                        this.el.setCounter(++this.count);
                        this.updated = true;
                        this.life = initialLife;
                    },
                    'setName' : function(name){
                        this.name = name;
                        this.el.setName(name);
                    },
                    'moveToTop' : function(){
                        //this.el.prependTo(hostsObj);
                    },
                    'address' : address,
                    'life' : initialLife
                };
                data[address] = o;
                var t = setInterval(function(){
                    o.life--;
                    if (o.life <= 0){
                        clearInterval(t);
                        o.el.fadeOut(config.boxFadeTime, function(){
                            o.el.remove();
                        });
                        delete data[address];
                    }
                }, 1000);

            }
            return data[address];
        };

        obj.getLatestUpdated = function(){
            var updated = [];
            $.each(data, function(_, o){
                if (o.updated){
                    updated.push(o);
                    o.updated = false;
                }
            });
            return updated;
        };

        return obj;
    }());

    var portsData = (function(){
        var obj = {}, data = {};

        obj.getPortObject = function(port){
            if (!(port in data)){
                data[port] = {
                    'el' : makeNewElement(port, portsObj),
                    'count' : 0,
                    'ondata' : function(){
                        this.el.setCounter(++this.count);
                    }
                };
            }
            return data[port];
        };

        return obj;
    }());

    var messageCount = 0;
    function showData(data, port){
        if (messageCount < config.maxMessages){
            messageCount++;
            var div = $('<div></div>');
            div.addClass('data').addClass('port' + port);
            div.text(data);
            div.css('top', Math.floor((Math.random() * 100)) + '%').css('z-index', 5);
            $('#main').append(div);
            setTimeout(function(){
                messageCount--;
                div.remove();
            }, config.messageSlideTime * 1000);
        }
    }

    var dataSource = new EventSource("data");
    dataSource.onmessage = function(e) {
          var obj = JSON.parse(e.data);
          var hostObj = hostsData.getHostObject(obj.host);
          hostObj.ondata();

          var portsObj = portsData.getPortObject(obj.port);
          portsObj.ondata();

          drawLine(hostObj.el.getIndex(), portsObj.el.getIndex());
          if (obj.data){
              showData(obj.data, obj.port);
          }
    };

    var dnsSource = new EventSource("dns");
    dnsSource.onmessage = function(e) {
        var obj = JSON.parse(e.data);
        hostsData.getHostObject(obj.host).setName(obj.name);
    };

    setInterval(function(){
        $.each(hostsData.getLatestUpdated(), function(_, o){
            o.moveToTop();
        });
    }, 1000);

//    setInterval(function(){
//        dataSource.onmessage({data:"{'host' : '1.2.3.4', 'port' : 80}"});
//    }, 1000);


});
