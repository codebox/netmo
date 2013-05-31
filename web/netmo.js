$(function(){
    var hostsObj = $('#hosts');
    var linesObj = $('#lines canvas');
    var portsObj = $('#ports');

    function makeNewElement(text, parent){
        var elName  = $('<span></span>');
        var elCount = $('<span></span>');
        var elObj   = $('<div></div>');
        elObj.append(elName, elCount);
        elName.text(text);
        elCount.text('0');
        parent.prepend(elObj);
        elObj.setCounter = function(count){
            elCount.text(count);
            //elObj.prependTo(parent);
        };
        elObj.setName = function(name){
            elName.text(name);
            elObj.addClass('hilite');
            setTimeout(function(){
                elObj.removeClass('hilite');
            }, 1000);
        };
        return elObj;
    }

    var hostsData = (function(){
        var obj = {}, data = {};

        obj.getHostObject = function(address){
            if (!(address in data)){
                data[address] = {
                    'el' : makeNewElement(address, hostsObj),
                    'count' : 0,
                    'ondata' : function(){
                        this.el.setCounter(++this.count);
                        this.updated = true;
                    },
                    'setName' : function(name){
                        this.name = name;
                        this.el.setName(name);
                    },
                    'moveToTop' : function(){
                        this.el.prependTo(hostsObj);
                    },
                    'address' : address
                };
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


    var dataSource = new EventSource("data");
    dataSource.onmessage = function(e) {
          var obj = eval('(' + e.data + ')');
          hostsData.getHostObject(obj.host).ondata();
          portsData.getPortObject(obj.port).ondata();
    };

    var dnsSource = new EventSource("dns");
    dnsSource.onmessage = function(e) {
        var obj = eval('(' + e.data + ')');
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
