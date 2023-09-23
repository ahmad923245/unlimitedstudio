function changeStatus(page_url, status, id, rurl) {
    console.log(page_url)
    $.ajax({
        url: page_url,
        type: 'get',
        data: {
            'status': status,
            'id': id
        },
        success: function (res){
            if (res.status === 'success'){
                Toast.fire({
                  icon: 'success',
                  title: 'Updated successfully'
                })
            }else if (res.status === 'failed'){
                Toast.fire({
                  icon: 'error',
                  title: 'Something went wrong, please try again.'
                })
            }
        },
        error: function (data) {
            return false;
        }
    });
}

function deleteRecored(url, base_url,data) {
    $.ajax({
        url: url,
        type: 'get',
        success: function (res){
            if (res.status === 'success'){
                Toast.fire({
                  icon: 'success',
                  title: 'Record deleted successfully'
                })
            }else if (res.status === 'failed'){
                Toast.fire({
                  icon: 'error',
                  title: 'Something went wrong, please try again.'
                })
            }
        },
        error: function (data) {
            return false;
        }
    });
}
