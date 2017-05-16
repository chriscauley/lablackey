<conference-days>
  <ul class="tabs z-depth-1 tabs-fixed-width">
    <li class="tab" each={ uR.conf.days }>
      <a onclick={ select } class={ active: active }>{ verbose }</a></li>
  </ul>
  <div class="tab-content { active: active }" each={ uR.conf.days }>
    <div each={ block in blocks } class="block">
      <div class="occurrence" each={ block }>
        <div class="occurrence card">
          <div class="card-content">
            <div class="name">{ name }</div>
            <div if={ event.owners.length }>by { event.owners[0].first_name } { event.owners[0].last_name }</div>
            <div class="time">{ time_string }</div>
          </div>
        </div>
      </div>
      <hr/>
    </div>
  </div>

  select(e) {
    uR.forEach(uR.conf.days,function(d,i) {
      d.active = e.item.index == i;
    });
    this.update();
  }

  this.on("mount",function() {
    this.ajax({
      url: '/event/conference.json',
      success: function(data) {
        uR.conf = {};
        uR.conf.days = [];
        var days_map = {};
        var owners_map = {};
        var events = {};
        var block, last_start;
        uR.forEach(data.owners,function(owner) { owners_map[owner.id] = owner });
        uR.forEach(data.events,function(event) {
          event.owners = event.owner_ids.map(function(id) { return owners_map[id]});
          events[event.id] = event;
        });
        uR.forEach(data.eventoccurrences,function(occ) {
          occ.event = events[occ.event_id];
          occ.start_moment = moment(occ.start);
          occ.end_moment = moment(occ.end);
          var day = occ.start_moment.format("YYYY-MM-DD");
          occ.time_string = uR.formatTimeRange(occ.start,occ.end);
          if (!days_map[day]) {
            block = undefined;
            days_map[day] = {
              verbose: occ.start_moment.format("dddd Do"),
              blocks: [],
            }
          }
          if (last_start != occ.start_moment.format("HHmm")) {
            last_start = occ.start_moment.format("HHmm");
            if (block) { days_map[day].blocks.push(block) }
            block = [];
          }
          block.push(occ);
        });
        for (key in days_map) { uR.conf.days.push(days_map[key]); }
        uR.forEach(uR.conf.days,function(d,i) { d.index = i; });
        uR.conf.days[0].active = true;
      }
    });
  });

</conference-days>
