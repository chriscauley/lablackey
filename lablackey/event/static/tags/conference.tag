<conference-days>
  <ul class="tabs z-depth-1 tabs-fixed-width">
    <li class="tab" each={ days }>
      <a onclick={ select } class={ active: active }>{ start.hdate() }</a></li>
  </ul>
  <div class="tab-content { active: active }" each={ days }>
    <div class="column" each={ rooms }>
      <div class="room">{ name }</div>
      <div class="occurrence card " each={ occurrences }>
        <div class="card-content">
          <div class="name">{ artist.name }</div>
          <div class="time">{ start.htime() } - { end.htime() }</div>
        </div>
      </div>
    </div>
  </div>

  select(e) {
    uR.forEach(this.days,function(d,i) {
      d.active = e.item.index == i;
    });
    this.update();
  }

  this.on("mount",function() {
    function sortObject(obj,attr_name) {
      attr_name = attr_name || "_sort_attr";
      var keys = Object.keys(obj);
      keys.sort();
      return keys.map(function(key) {
        obj[key][attr_name] = key;
        return obj[key];
      })
    }
    this.ajax({
      url: '/event/conference.json',
      success: function(data) {
        var maps = {};
        var days_map = {};
        uR.forEach(['rooms','events','artists'],function(attr) {
          maps[attr] = {}
          uR.forEach(data[attr],function(obj) {
            maps[attr][obj.id] = obj;
          })
        });
        uR.forEach(data.eventoccurrences,function(occurrence) {
          var _d = occurrence.start.date();
          days_map[_d] = days_map[_d] || {
            occurrences: [],
            moment: moment(new Date(_d)),
            rooms: [],
          }
          occurrence.event = maps.events[occurrence.event_id];
          occurrence.room = maps.rooms[occurrence.event.room_id];
          occurrence.artist = occurrence.extra && maps.artists[occurrence.extra.artist];
          days_map[_d].verbose = days_map[_d].moment.format("MMM Do");
          days_map[_d].occurrences.push(occurrence);
        });
        this.days = sortObject(days_map,"date");
        uR.forEach(this.days,function(day,i) {
          day.index = i;
          day.occurrences.sort((o) => o.start)
          day.start = day.occurrences[0].start;
          day.sorted_occurrences = [];
          data.rooms.map(function(room) {
            var _r = {};
            uR.extend(_r,room);
            _r.occurrences = day.occurrences.filter((o) => o.room.id==_r.id );
            _r.occurrences.length && day.rooms.push(_r);
            _r.occurrences.sort((o) => o.start)
          });
        });
        this.days[0].active = true;
      }
    });
  });
</conference-days>
