/*jslint plusplus: true */
/*global $,window*/
$(function() {
    "use strict";

    var hostsObj = $('#hosts'),
        linesObj = $('#lines'),
        svgObj = $('#lines svg'),
        portsObj  = $('#ports'),
        blockHeight = 34,
        svgWidth = svgObj.width(),
        maxHosts = 10,
        hostsData,
        portsData,
        messageCount,
        dataSource,
        dnsSource,

        config = {
            hiliteFade: 1000,
            lineWidth : '1',
            lineFadeDelta : 0.1,
            boxFadeTime : 2000,
            messageSlideTime: 10,
            maxMessages: 10,
            lineColour: '#555'
        };

    function makeNewElement(text, parent) {
        var elName  = $('<span></span>'),
            elCount = $('<span></span>'),
            elObj   = $('<div></div>');
        elObj.append(elName, elCount);
        elName.text(text);

        parent.append(elObj);
        elObj.setCounter = function(count) {
            //elCount.text(count);
            //elObj.prependTo(parent);
        };
        elObj.setName = function(name) {
            elName.text(name);
            elObj.addClass('hilite');
            window.setTimeout(function() {
                elObj.removeClass('hilite');
            }, config.hiliteFade);
        };
        elObj.getIndex = function() {
            return parent.find('div').index(elObj);
        };
        elObj.css('z-index', 10);
        return elObj;
    }

    function drawLine(hostIndex, portIndex) {
        var path = $(window.document.createElementNS("http://www.w3.org/2000/svg", 'path')),
            startY = (hostIndex + 0.5) * blockHeight,
            endY = (portIndex + 0.5) * blockHeight,
            opacity = 1,
            delta = config.lineFadeDelta,
            interval = window.setInterval(function() {
                opacity -= delta;
                path.attr('stroke-opacity', opacity);
                if (opacity <= 0) {
                    window.clearInterval(interval);
                    path.remove();
                }
            }, 50);

        path.attr('d', ['m 0,', startY, ' c 50,0 150,', (endY - startY), ' ', svgWidth, ',', (endY - startY)].join(''));
        path.attr('stroke', config.lineColour);
        path.attr('fill', 'none');
        path.attr('stroke-width', config.lineWidth);
        svgObj.append(path);
    }

    hostsData = (function() {
        var obj = {}, data = {};

        obj.getHostObject = function(address) {
            if (!(data.hasOwnProperty(address))) {
                var initialLife = 10,
                    o  = {
                        'el' : makeNewElement(address, hostsObj),
                        'count' : 0,
                        'ondata' : function() {
                            this.el.setCounter(++this.count);
                            this.updated = true;
                            this.life = initialLife;
                        },
                        'setName' : function(name) {
                            this.name = name;
                            this.el.setName(name);
                        },
                        'moveToTop' : function() {
                            //this.el.prependTo(hostsObj);
                        },
                        'address' : address,
                        'life' : initialLife
                    },
                    t = window.setInterval(function() {
                        o.life--;
                        if (o.life <= 0) {
                            window.clearInterval(t);
                            o.el.fadeOut(config.boxFadeTime, function() {
                                o.el.remove();
                            });
                            delete data[address];
                        }
                    }, 1000);
                data[address] = o;
            }
            return data[address];
        };

        obj.getLatestUpdated = function() {
            var updated = [];
            /*jslint unparam: true*/
            $.each(data, function(ignore, o) {
                if (o.updated) {
                    updated.push(o);
                    o.updated = false;
                }
            });
            /*jslint unparam: false*/
            return updated;
        };

        return obj;
    }());

    portsData = (function() {
        var obj = {}, data = {};

        obj.getPortObject = function(port) {
            if (!(data.hasOwnProperty(port))) {
                data[port] = {
                    'el' : makeNewElement(port, portsObj),
                    'count' : 0,
                    'ondata' : function() {
                        this.el.setCounter(++this.count);
                    }
                };
            }
            return data[port];
        };

        return obj;
    }());

    messageCount = 0;
    function showData(data, port) {
        if (messageCount < config.maxMessages) {
            messageCount++;
            var div = $('<div></div>');
            div.addClass('data').addClass('port' + port);
            div.text(data);
            div.css('top', Math.floor((Math.random() * 50) + 50) + '%').css('z-index', 7);
            $('#main').append(div);
            window.setTimeout(function() {
                messageCount--;
                div.remove();
            }, config.messageSlideTime * 1000);
        }
    }

    dataSource = new window.EventSource("data");
    dataSource.onmessage = function(e) {
        var obj = JSON.parse(e.data),
            hostObj = hostsData.getHostObject(obj.host),
            portsObj = portsData.getPortObject(obj.port);

        hostObj.ondata();
        portsObj.ondata();

        drawLine(hostObj.el.getIndex(), portsObj.el.getIndex());
        if (obj.data) {
            showData(obj.data, obj.port);
        }
    };
    
    dnsSource = new window.EventSource("dns");
    dnsSource.onmessage = function(e) {
        var obj = JSON.parse(e.data);
        hostsData.getHostObject(obj.host).setName(obj.name);
    };

    window.setInterval(function() {
        $.each(hostsData.getLatestUpdated(), function(_, o){
            o.moveToTop();
        });
    }, 1000);

//    setInterval(function(){
//        dataSource.onmessage({data:"{'host' : '1.2.3.4', 'port' : 80}"});
//    }, 1000);


});
