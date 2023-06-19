const data = [
  {
    brand: "hãng xe",
    samples: [
      {
        name: "tên",
        price: "1000",
        address: "địa chỉ",
        url: "link gốc",
        registerYear: "năm đăng ký",
        status: "mới",
        type: "loại xe",
        capacity: "dung tích xe máy",
        origin: "xuất xứ",
        color: "màu xe",
        vehicleType: "dòng xe",
        km: "số km đã đi",
      },
      {
        name: "tên",
        price: "1000",
        address: "địa chỉ",
        url: "link gốc",
        registerYear: "năm đăng ký",
        status: "mới",
        type: "loại xe",
        capacity: "dung tích xe máy",
        origin: "xuất xứ",
        color: "màu xe",
        vehicleType: "dòng xe",
        km: "số km đã đi",
      },
    ],
  },
];

var Render = new (function __Render() {
  this.init = function () {
    var motobikes = [];
    var categories = [];
    // $.ajax({
    // 	url: 'http://127.0.0.1:5000/api/list',
    // 	success: function (data) {
    // 		data.forEach(function (category) {
    // 			categories.push(category.brand);
    // 			category.samples.forEach(function (motobike) {
    // 				motobikes.push(motobike);
    // 			});
    // 		});
    // 	},
    // 	async: false
    // });
    data.forEach(function (category) {
      categories.push(category.brand);
      category.samples.forEach(function (motobike) {
        motobikes.push(motobike);
      });
    });

    return [categories, motobikes];
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
    <div class=""card shadow-sm p-3 mb-5 bg-white rounded" style = "width: 18rem;">
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

$("#search").on("keyup", function () {
  var value = $(this).val().toLowerCase();
  var rs = motobikes.filter((motobike) =>
    motobike.name.toLowerCase().includes(value)
  );
  Render.cards(rs);
});

$("#min-price").on("keyup", function () {
  var name = $("#search").val().toLowerCase();
  var rs = motobikes;
  if (name) {
    rs = motobikes.filter((motobike) =>
      motobike.name.toLowerCase().includes(name)
    );
  }

  var min_price = parseInt($(this).val() + "000000");
  if (isNaN(min_price) || min_price == 0) {
    Render.cards(rs);
    return;
  }
  var max_price = parseInt($("#max-price").val() + "000000");
  if (isNaN(max_price) || max_price == 0) {
    rs = rs.filter((motobike) => motobike.price >= min_price);
    Render.cards(rs);
  } else {
    var rs = rs.filter(
      (motobike) =>
        motobike.price >= min_price && motobike.price <= max_price
    );
    Render.cards(rs);
  }
});

$("#max-price").on("keyup", function () {
  var name = $("#search").val().toLowerCase();
  var rs = motobikes;
  if (name) {
    rs = motobikes.filter((motobike) =>
      motobike.name.toLowerCase().includes(name)
    );
  }

  var max_price = parseInt($(this).val() + "000000");
  if (isNaN(max_price) || max_price == 0) {
    Render.cards(rs);
    return;
  }
  var min_price = parseInt($("#min-price").val() + "000000");
  if (isNaN(min_price) || min_price == 0) {
    var rs = rs.filter((motobike) => motobike.price <= max_price);
    Render.cards(rs);
  } else {
    var rs = rs.filter(
      (motobike) =>
        motobike.price >= min_price && motobike.price <= max_price
    );
    Render.cards(rs);
  }
});

var [categories, motobikes] = Render.init();
Render.cards(motobikes);
