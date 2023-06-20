var Render = new (function __Render() {
  this.init = function () {
    var motobikes = [];
    $.ajax({
    	url: 'http://127.0.0.1:5000/api/list',
    	success: function (data) {
        data.forEach(function (dat) {
          motobikes.push(dat);
        });
    	},
    	async: false
    });

    return motobikes;
  };

  this.cards = function (motobikes) {
    var html = ``;

    motobikes.forEach(function (motobike) {
      html += getHTML(motobike);
    });
    $("#products").html(html);
  };
})();

function getHTML(motobike) {
  var price = formatCash(String(motobike.price));
  return `
  <div class="col-12 col-sm-6 col-md-4 margin">
    <div class="card shadow-sm p-3 mb-5 bg-white rounded" style = "width: 18rem;">
      <img src="${motobike.image_url}" class="card-img-top" alt="Image">
      <div class="card-body">
        <h2 class="card-title">${motobike.name}</h2>
        <ul class="list-group list-group-flush">
          <li class="list-group-item"><span>Địa chỉ: </span>${motobike.address}</li>
          <li class="list-group-item"><span>Năm đăng ký: </span>${motobike.registerYear}</li>
          <li class="list-group-item"><span>Trạng thái: </span>${motobike.status}</li>
          <li class="list-group-item"><span>Loại xe: </span>${motobike.type}</li>
          <li class="list-group-item"><span>Dung tích: </span>${motobike.capacity}</li>
          <li class="list-group-item"><span>Xuất xứ: </span>${motobike.origin}</li>
          <li class="list-group-item"><span>Màu: </span>${motobike.color}</li>
          <li class="list-group-item"><span>Dòng xe: </span>${motobike.vehicleType}</li>
          <li class="list-group-item"><span>Số km đã đi: </span>${motobike.km}</li>
        </ul>
      </div>
      <div class="text-center">
        <p class="card-footer display-5"><span >Giá: </span>${motobike.price}</p>
        <a href="${motobike.url}" class="btn btn-primary">Mua</a>
      </div>
    </div>
  </div>
	`;
}

function formatCash(str) {
  return (
    str
      .split("")
      .reverse()
      .reduce((prev, next, index) => {
        return (index % 3 ? next : next + ",") + prev;
      }) + " VND"
  );
}

$("#search-btn").on("click", function () {
  var name = $("#search").val().toLowerCase();
  var min_price = parseInt($("#min-price").val() + "000000");
  var max_price = parseInt($("#max-price").val() + "000000");
  var motobikes = [];
  $.ajax({
    url: 'http://127.0.0.1:5000/api/search?name=' + name + '&min_price=' + min_price + '&max_price=' + max_price,
    success: function (data) {
      data.forEach(function (dat) {
        motobikes.push(dat);
      });
    },
    async: false
  });
  Render.cards(motobikes);
});

var motobikes = Render.init();
Render.cards(motobikes);
