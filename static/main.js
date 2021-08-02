


// (function($) {
//     $(function(){
//         $.ajax({
//             type: 'GET',
//             url: '/api/get_attendance',
//             success: function(data){
//                 console.log('success', data)
//             }
//         })
//     })
// })(jQuery);

function addOptions( fromId, toId ) {
    var fromEl = document.getElementById( fromId ),
        toEl = document.getElementById( toId );

    if ( fromEl.selectedIndex >= 0 ) {
        var index = toEl.options.length;

        for ( var i = 0; i < fromEl.options.length; i++ ) {
            if ( fromEl.options[ i ].selected ) {
                toEl.options[ index ] = fromEl.options[ i ];
                i--;
                index++
            }
        }
    }
}