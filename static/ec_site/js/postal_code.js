document.addEventListener('DOMContentLoaded', function() {
    var autoFillButton = document.getElementById('auto_fill_address');
    if (autoFillButton) {
        autoFillButton.addEventListener('click', function() {
            var postalCodeInput = document.getElementById('postal_code');
            var postalCode = postalCodeInput.value.replace(/-/g, ''); // ハイフンを除去
            if (postalCode.length === 7) {
                var request = new XMLHttpRequest();
                request.open('GET', 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=' + postalCode, true);
                request.onreadystatechange = function() {
                    if (request.readyState === 4 && request.status === 200) {
                        var response = JSON.parse(request.responseText);
                        if (response.results) {
                            document.getElementById('prefectures').value = response.results[0].address1;
                            document.getElementById('city').value = response.results[0].address2;
                            document.getElementById('address_line1').value = response.results[0].address3;
                        }
                    }
                };
                request.send();
            }
        });
    }
});