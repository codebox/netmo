window.onload = function(){
    var l = document.getElementById('list');
    var h = document.getElementById('host');
    var portData = {}, hostData = {};

    function addPort(port, count){
        if (! portData[port]){
	        var li = document.createElement('li');
	        li.className = 'box';
	        l.appendChild(li);
        	portData[port] = {'count' : 0, 'el' : li};
        }
        portData[port].count += count;
        portData[port].el.innerHTML = 'Port ' + port + '<br>' + portData[port].count;
    }
    function addHost(ip,host){
        if (! hostData[ip]){
            var li = document.createElement('li');
            h.appendChild(li);
            hostData[ip] = {'count' : 0, 'el' : li};
        }
        hostData[ip].count += 1;
        hostData[ip].el.innerHTML = host + ': ' + hostData[ip].count;
    }

    var evtSource = new EventSource("data");
    evtSource.onmessage = function(e) {
          var obj = eval('(' + e.data + ')');
          addPort(Number(obj.dport), 1);
          addHost(obj.src, obj.host);
    };

}
