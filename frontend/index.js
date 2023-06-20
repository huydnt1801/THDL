var Render = new (function __Render() {
  this.total = function (){
    const urlParams = new URLSearchParams(window.location.search);
    const myParam = urlParams.get('page');
    var i = 1;
    if (myParam != undefined) {
      i = parseInt(myParam, 10);
    }
    var t = 0;
    $.ajax({
      type: 'GET',
    	url: 'http://127.0.0.1:5000/api/total',
    	success: function (data) {
        t = Math.ceil(data / 18);
    	},
    	async: false
    });
    if (i > t - 4) {
      i = 1;
    }
    var pag = "";
    var j = 0;
    while (j < 2) {
      pag += `<li onclick="changePage(${i+j})"><a>${i+j}</a></li>`
      j++;
    };
    pag += `<li><a>...</a></li>`;
    var i = 1;
    while (i >= 0) {
      pag += `<li onclick="changePage(${t-i})"><a>${t-i}</a></li>`
      i--;
    };
    $("#pagination").html(pag);
  }
  this.init = function () {
    var motobikes = [];
    const urlParams = new URLSearchParams(window.location.search);
    const myParam = urlParams.get('page');
    var i = 1;
    if (myParam != undefined) {
      i = parseInt(myParam, 10);
    }
    $.ajax({
      type: 'GET',
    	url: 'http://127.0.0.1:5000/api/list?page=' + i,
      contentType: 'application/json',
      dataType: 'json',
      complete: function(data) {
        console.log(data);
      },
    	success: function (data) {
        console.log(data);
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

function changePage(page) {
  var url = new URL(window.location.href);
  url.searchParams.set('page', page);
  window.location.href = url.href;
}

function getHTML(motobike) {
  var price = formatCash(String(motobike.price));
  let addressItem = '';
  if (motobike.address !== undefined) {
    addressItem = `<li class="list-group-item"><span>Địa chỉ: </span>${motobike.address}</li>`;
  }
  let registerYearItem = '';
  if (motobike.registerYear !== undefined) {
    registerYearItem = `<li class="list-group-item"><span>Năm đăng ký: </span>${motobike.registerYear}</li>`;
  }
  let statusItem = '';
  if (motobike.status !== undefined) {
    statusItem = `<li class="list-group-item"><span>Trạng thái: </span>${motobike.status}</li>`;
  }
  let typeItem = '';
  if (motobike.type !== undefined) {
    typeItem = `<li class="list-group-item"><span>Loại xe: </span>${motobike.type}</li>`;
  }
  let capacityItem = '';
  if (motobike.capacity !== undefined) {
    capacityItem = `<li class="list-group-item"><span>Dung tích: </span>${motobike.capacity}</li>`;
  }
  let originItem = '';
  if (motobike.origin !== undefined) {
    originItem = `<li class="list-group-item"><span>Xuất xứ: </span>${motobike.origin}</li>`;
  }
  let colorItem = '';
  if (motobike.color !== undefined) {
    colorItem = `<li class="list-group-item"><span>Màu sắc: </span>${motobike.color}</li>`;
  }
  let vehicleTypeItem = '';
  if (motobike.vehicleType !== undefined) {
    vehicleTypeItem = `<li class="list-group-item"><span>Dòng xe: </span>${motobike.vehicleType}</li>`;
  }
  let kmItem = '';
  if (motobike.km !== undefined) {
    kmItem = `<li class="list-group-item"><span>Số km đã đi: </span>${motobike.km}</li>`;
  }
  return `
  <div class="col-12 col-sm-6 col-md-4 margin">
    <div class="card shadow-sm p-3 mb-5 bg-white rounded" style = "width: 18rem;">
      <img src="${motobike.image_url}" class="card-img-top" alt="Image">
      <div class="card-body">
        <h6 class="card-title">${motobike.name}</h6>
        <ul class="list-group list-group-flush">
          ${addressItem}
          ${registerYearItem}
          ${statusItem}
          ${typeItem}
          ${capacityItem}
          ${originItem}
          ${colorItem}
          ${vehicleTypeItem}
          ${kmItem}
        </ul>
      </div>
      <div class="text-center">
        <p class="card-footer display-5"><span >Giá: </span>${price}</p>
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
    url: 'http://127.0.0.1:5000/api/search?name=' + name + '&minPrice=' + min_price + '&maxPrice=' + max_price,
    success: function (data) {
      data.forEach(function (dat) {
        motobikes.push(dat);
      });
    },
    async: false
  });
  Render.cards(motobikes);
});

Render.total();
var motobikes = Render.init();
Render.cards(motobikes);
