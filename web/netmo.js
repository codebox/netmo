window.onload = function(){
    var l = document.getElementById('list');
    var h = document.getElementById('host');
    var data = {};

    function addPort(port, count){
        if (! data[port]){
	        var li = document.createElement('li');
	        li.className = 'box';
	        l.appendChild(li);
        	data[port] = {'count' : 0, 'el' : li};
        }
        data[port].count += count;
        data[port].el.innerHTML = 'Port ' + port + '<br>' + data[port].count;
    }
    function addHost(host){
        var li = document.createElement('li');
        h.appendChild(li);
        li.innerHTML = host;
    }

    var evtSource = new EventSource("data");
    evtSource.onmessage = function(e) {
          var obj = eval('(' + e.data + ')');
          addPort(Number(obj.dport), 1);
          addHost(obj.src);
    };

}
