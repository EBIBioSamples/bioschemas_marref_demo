// Pop-up image preview for "Documentation" and "Help", with img source link kept
$(window).on('load', function() {
    $(function() {
        $.each($(this).find('#container-contact-text').find('a'), function() {
            if($(this).find('> img').length)
            {
                $(this).attr('href', $(this).find('> img').attr('src'));
                $(this).on('click', function() {
                    $('#imagepreview').attr('src', $(this).find('> img').attr('src'));
                    $('#imagemodal').modal('show');   
                    return false;
                });
            }
        });
    });
});

