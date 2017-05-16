<conference-days>
  <div>what the butt</div>
  <div class="tab" each={ uR.conf.days }>{ verbose }</div>
  <div class="tab-content" each={ uR.conf.days }>
    <div each={ occurrences } class="occurrence">
      <div class="name">{ name }</div>
      <div if={ event.owners.length }>by { event.owners[0].first_name } { event.owners[0].last_name }</div>
      <div class="time">{ time_string }</div>
    </div>
  </div>


  this.on("mount",function() {
    this.ajax({
      url: '/event/conference.json',
      success: function(data) {
        uR.conf = {};
        uR.conf.days = [];
        var days_map = {};
        var owners_map = {};
        var events = {};
        uR.forEach(data.owners,function(owner) { owners_map[owner.id] = owner });
        uR.forEach(data.events,function(event) {
          event.owners = event.owner_ids.map(function(id) { return owners_map[id]});
          events[event.id] = event;
        });
        console.log(owners_map);
        uR.forEach(data.eventoccurrences,function(occ) {
          occ.event = events[occ.event_id];
          occ.start_moment = moment(occ.start);
          occ.end_moment = moment(occ.end);
          var day = occ.start_moment.format("YYYY-MM-DD");
          occ.time_string = uR.formatTimeRange(occ.start,occ.end);
          if (!days_map[day]) {
            days_map[day] = {
              verbose: occ.start_moment.format("dddd Do"),
              occurrences: [],
            }
          }
          days_map[day].occurrences.push(occ)
        });
        for (key in days_map) { uR.conf.days.push(days_map[key]); }
      }
    });
  });

</conference-days>

<event-day>
  <div each={ opts.occurrences }>{ name }</div>

console.log(this.opts);
</event-day>
