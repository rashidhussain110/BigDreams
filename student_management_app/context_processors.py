def announcement_count(request):
    # Gives every page the number of announcements this staff member or student has not opened yet
    if request.user.is_authenticated and str(request.user.user_type) in ("2", "3"):
        from .models import Announcement, AnnouncementRead

        read_ids = AnnouncementRead.objects.filter(user=request.user).values_list('announcement_id', flat=True)
        count = Announcement.objects.exclude(id__in=read_ids).count()
        return {"unread_announcements": count}
    return {}