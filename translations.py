from flask import session

# Translation dictionary
translations = {
    'en': {
        # Navigation
        'home': 'Home',
        'archive': 'Archive',
        'info': 'Info',
        'appeal': 'Appeal',
        'admin': 'Admin',
        'language': 'Language',
        
        # Home page
        'weekly_topic': 'Weekly Topic',
        'weekly_story': 'Weekly Story',
        'comments': 'Comments',
        'post_comment': 'Post Comment',
        'name': 'Name',
        'email': 'Email (optional)',
        'comment': 'Comment',
        'comment_language': 'Comment Language',
        'english': 'English',
        'persian': 'فارسی',
        'like': 'Like',
        'dislike': 'Dislike',
        'reply': 'Reply',
        'no_comments': 'No comments yet. Be the first to comment!',
        'comment_posted': 'Comment posted successfully!',
        'comment_hidden': 'This comment has been hidden due to community feedback.',
        
        # Archive page
        'discussion_archive': 'Discussion Archive',
        'download_pdf': 'Download PDF',
        'no_topics': 'No topics available.',
        
        # Info page
        'about_platform': 'About Project Dard',
        'platform_description': 'Project Dard is a community platform for academic discussions and knowledge sharing.',
        'founder': 'Founder',
        'team': 'Team',
        'featured_author': 'Featured Author',
        
        # Appeal page
        'appeal_form': 'Appeal Form',
        'appeal_description': 'If your comment was hidden, you can submit an appeal here.',
        'your_name': 'Your Name',
        'your_email': 'Your Email',
        'reason_for_appeal': 'Reason for Appeal',
        'submit_appeal': 'Submit Appeal',
        'appeal_submitted': 'Appeal submitted successfully!',
        'contact_info': 'Contact Information',
        'social_media': 'Social Media',
        
        # Admin
        'login': 'Login',
        'username': 'Username',
        'password': 'Password',
        'remember_me': 'Remember Me',
        'sign_in': 'Sign In',
        'dashboard': 'Dashboard',
        'statistics': 'Statistics',
        'recent_activity': 'Recent Activity',
        'manage_comments': 'Manage Comments',
        'post_topic': 'Post Topic',
        'post_story': 'Post Story',
        'logout': 'Logout',
        
        # Messages
        'invalid_credentials': 'Invalid username or password',
        'access_denied': 'Access denied',
        'invalid_comment': 'Invalid comment reference',
        'comment_not_hidden': 'Comment is not hidden',
        'topic_posted': 'Topic posted successfully!',
        'story_posted': 'Story posted successfully!',
        
        # Form labels
        'title_english': 'Title (English)',
        'title_persian': 'Title (Persian)',
        'content_english': 'Content (English)',
        'content_persian': 'Content (Persian)',
        'author_english': 'Author (English)',
        'author_persian': 'Author (Persian)',
    },
    'fa': {
        # Navigation
        'home': 'خانه',
        'archive': 'آرشیو',
        'info': 'اطلاعات',
        'appeal': 'درخواست بازبینی',
        'admin': 'مدیریت',
        'language': 'زبان',
        
        # Home page
        'weekly_topic': 'موضوع هفته',
        'weekly_story': 'داستان هفته',
        'comments': 'نظرات',
        'post_comment': 'ارسال نظر',
        'name': 'نام',
        'email': 'ایمیل (اختیاری)',
        'comment': 'نظر',
        'comment_language': 'زبان نظر',
        'english': 'English',
        'persian': 'فارسی',
        'like': 'پسند',
        'dislike': 'نپسند',
        'reply': 'پاسخ',
        'no_comments': 'هنوز نظری ثبت نشده. اولین نفر باشید!',
        'comment_posted': 'نظر شما با موفقیت ارسال شد!',
        'comment_hidden': 'این نظر به دلیل بازخورد منفی جامعه مخفی شده است.',
        
        # Archive page
        'discussion_archive': 'آرشیو بحث‌ها',
        'download_pdf': 'دانلود PDF',
        'no_topics': 'موضوعی موجود نیست.',
        
        # Info page
        'about_platform': 'درباره پروژه درد',
        'platform_description': 'پروژه درد پلتفرمی برای بحث‌های آکادمیک و اشتراک دانش است.',
        'founder': 'بنیان‌گذار',
        'team': 'تیم',
        'featured_author': 'نویسنده برگزیده',
        
        # Appeal page
        'appeal_form': 'فرم درخواست بازبینی',
        'appeal_description': 'اگر نظر شما مخفی شده، می‌توانید درخواست بازبینی ارسال کنید.',
        'your_name': 'نام شما',
        'your_email': 'ایمیل شما',
        'reason_for_appeal': 'دلیل درخواست بازبینی',
        'submit_appeal': 'ارسال درخواست',
        'appeal_submitted': 'درخواست شما با موفقیت ارسال شد!',
        'contact_info': 'اطلاعات تماس',
        'social_media': 'شبکه‌های اجتماعی',
        
        # Admin
        'login': 'ورود',
        'username': 'نام کاربری',
        'password': 'رمز عبور',
        'remember_me': 'مرا به خاطر بسپار',
        'sign_in': 'ورود',
        'dashboard': 'داشبورد',
        'statistics': 'آمار',
        'recent_activity': 'فعالیت‌های اخیر',
        'manage_comments': 'مدیریت نظرات',
        'post_topic': 'ارسال موضوع',
        'post_story': 'ارسال داستان',
        'logout': 'خروج',
        
        # Messages
        'invalid_credentials': 'نام کاربری یا رمز عبور اشتباه است',
        'access_denied': 'دسترسی مجاز نیست',
        'invalid_comment': 'ارجاع نظر نامعتبر است',
        'comment_not_hidden': 'نظر مخفی نشده است',
        'topic_posted': 'موضوع با موفقیت ارسال شد!',
        'story_posted': 'داستان با موفقیت ارسال شد!',
        
        # Form labels
        'title_english': 'عنوان (انگلیسی)',
        'title_persian': 'عنوان (فارسی)',
        'content_english': 'محتوا (انگلیسی)',
        'content_persian': 'محتوا (فارسی)',
        'author_english': 'نویسنده (انگلیسی)',
        'author_persian': 'نویسنده (فارسی)',
    }
}

def get_text(key, language=None):
    """Get translated text for a key"""
    if language is None:
        language = session.get('language', 'en')
    
    return translations.get(language, {}).get(key, translations['en'].get(key, key))

def get_supported_languages():
    """Get list of supported languages"""
    return list(translations.keys())
