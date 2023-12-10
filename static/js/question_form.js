$(document).ready(function() {
    $('#faculty-select').change(function() {
        var facultyId = $(this).val();
        if (facultyId) {
            console.log(facultyId);
            $.ajax({
                url: '/qanda/get_departments/' + facultyId + '/',
                type: 'GET',
                dataType: 'json',
                success: function(data) {
                    $('#department-select').empty();
                    $('#department-select').append('<option value="">選択してください</option>');
                    $.each(data, function(key, value) {
                        $('#department-select').append('<option value="' + key + '">' + value.department + '</option>');
                    });
                }
            });
        } else {
            $('#department-select').empty();
            $('#department-select').append('<option value="">選択してください</option>');
        }
    });
});