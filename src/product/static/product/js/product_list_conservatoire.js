// Filter function
$(document).ready(function(){
    // url path before page index
    var url_path1 = '';
    url_path1 += url_product_api_product_list + '?category=' + category_id + '&' + 'page=';
    // console.log(url_path1);

    $('#product-list-is').infiniteScroll({
        path: function() {
            var pageIndex = this.loadCount + 1;
            // console.log(url_path1 + pageIndex);
            return url_path1 + pageIndex;
        },
        responseType: 'text',
        scrollThreshold: 1000,
        status: '.page-load-status',
        history: false,
        debug: false,
    });
    infiniteMode = 'load.infiniteScroll';

    $('#product-list-is').on(infiniteMode, function(event, response, path) {
        // parse response into JSON data
        var data = JSON.parse(response);
        // console.log(data);
        if (data.count > 1) {
            $('#mm-is-result-count1').html(data.count);
            $('#mm-is-result-count2').show();
            $('#mm-is-result-count4').hide();
            $('#mm-is-result-count3').show();
        } else {
            $('#mm-is-result-count1').html(data.count);
            $('#mm-is-result-count2').show();
            $('#mm-is-result-count3').hide();
            $('#mm-is-result-count4').show();
        }
        if (data.count == 0) {
            // console.log('no data found');
            $('.mm-is-loader').css('display','none');
            $('#product-list-is').infiniteScroll('destroy');
        } else {
            // compile data into HTML
            var itemsHTML = data.results.map(getSingleProductBlock).join('');
            // convert HTML string into elements
            var $items = $(itemsHTML);
            // append item elements
            $items.imagesLoaded( function() {
                $('#product-list-is').infiniteScroll('appendItems', $items);
            });
        }
        if (data.count != 0 && data.next == null) {
            // console.log('no more data');
            $('.mm-is-loader').css('display','none');
            $('.mm-is-last').css('display','block');
            $('#product-list-is').infiniteScroll('destroy');
        }
    });

    $('#product-list-is').infiniteScroll('loadNextPage');
});

// function productList(){
//
// }
