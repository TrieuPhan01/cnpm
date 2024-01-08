document.addEventListener('DOMContentLoaded', function () {
    // Lắng nghe sự kiện thay đổi trạng thái của radio button
    document.querySelectorAll('input[name="ticketType"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            // Nếu chọn "Vé một chiều", ẩn trường nhập ngày về
            if (radio.id === 'ticketType-1') {
                document.getElementById('returnDateContainer').style.display = 'none';
            } else {
                // Nếu chọn "Vé khứ hồi", hiện trường nhập ngày về
                document.getElementById('returnDateContainer').style.display = 'block';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Lắng nghe sự kiện thay đổi trạng thái của radio button
    document.querySelectorAll('input[name="ticketType"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            // Nếu chọn "Vé một chiều", ẩn trường nhập ngày về
            if (radio.id === 'ticketType-1') {
                document.getElementById('returnDateContainer').style.display = 'none';
            } else {
                // Nếu chọn "Vé khứ hồi", hiện trường nhập ngày về
                document.getElementById('returnDateContainer').style.display = 'block';
            }
        });
    });
});

// homeAndFindFlights.js
document.addEventListener("DOMContentLoaded", function () {
  var fromInput = document.getElementById("ap_from");
  var toInput = document.getElementById("ap_to");
  var airportsDataList = document.getElementById("airports");

  fromInput.addEventListener("input", function () {
    showAirportList(fromInput);
  });

  toInput.addEventListener("input", function () {
    showAirportList(toInput);
  });

  function showAirportList(input) {
    airportsDataList.innerHTML = "";

    // Fetch airport data from Flask endpoint
    fetch("/get_airports")
      .then(response => response.json())
      .then(data => {
        data.airports.forEach(function (airport) {
          var option = document.createElement("option");
          option.value = `${airport.id} - ${airport.name}`;
          airportsDataList.appendChild(option);
        });
      });
  }
});


    document.addEventListener('DOMContentLoaded', function () {
        document.getElementById('submit-btn').addEventListener('click', function (event) {
            var ticketType = document.querySelector('input[name="ticketType"]:checked');
            var fromInput = document.getElementById('ap_from');
            var toInput = document.getElementById('ap_to');
            var dayStartInput = document.getElementById('time_start');
            var returnDateInput = document.getElementById('return_date');
            var rankChairInput = document.getElementById('ticket_type');

            // Kiểm tra xem tất cả các trường đã được nhập đầy đủ chưa
            if (!ticketType || !fromInput.value || !toInput.value || !dayStartInput.value || (ticketType.value === '2' && !returnDateInput.value) || !rankChairInput.value) {
                alert('Vui lòng nhập đầy đủ thông tin để tìm kiếm chuyến bay.');
                event.preventDefault(); // Ngăn chặn sự kiện tìm kiếm nếu thông tin không đầy đủ
            }
        });
    });


function save(){
let data = {};
     data.ticketType = document.querySelector('input[name="ticketType"]:checked').value;
    data.fromLocation = document.getElementById('ap_from').value;
    data.toLocation = document.getElementById('ap_to').value;data.dayStart = document.getElementById('time_start').value;
    data.returnDate = document.getElementById('return_date').value;
    data.rankChair = document.getElementById('ticket_type').value;
     localStorage.setItem('DATA_INFO', JSON.stringify(data));
     console.log(data)
}
// Trong file homeAndFindFlights.js
function lay() {
    let data = JSON.parse(localStorage.getItem('DATA_INFO'));
    if (data) {
        // Tạo một đối tượng date từ chuỗi ngày
        let startDate = new Date(data.dayStart);

        // Định dạng lại ngày theo mong muốn (ví dụ: dd/MM/yyyy)
        let formattedStartDate = `${startDate.getDate()}/${startDate.getMonth() + 1}/${startDate.getFullYear()}`;

        // Hiển thị dữ liệu vào các thẻ div
        document.getElementById('fromTo').innerText = `${data.fromLocation} → ${data.toLocation}`;
//        document.getElementById('ap_to').innerText = data.toLocation;
        document.getElementById('dateInfo').innerText = `${formattedStartDate} | 1 hành khách | Vé hạng ${data.rankChair}`;
//        document.getElementById('ticket_type').innerText = `Vé hạng ${data.rankChair}`;
    }
}
