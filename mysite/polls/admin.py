import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Language, Word, UserResponse


def export_user_responses_to_csv(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="user_responses.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(["User Session", "Word", "Response", "Timestamp", "Difficulty"])

    # Write data rows
    for user_response in queryset:
        writer.writerow(
            [
                user_response.user_session,
                user_response.word.lemma,
                user_response.response,
                user_response.timestamp,
                user_response.word.difficulty,
            ]
        )

    return response


export_user_responses_to_csv.short_description = "Export selected responses to CSV"


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ("user_session", "word", "response", "timestamp")
    list_filter = ("user_session",)  # Add filter by user_session
    actions = [export_user_responses_to_csv]


admin.site.register(Language)
admin.site.register(Word)
