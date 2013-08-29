from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import DiffLexer

from reviewboard.diffviewer.models import FileDiff, DiffSet, DiffSetHistory


class FileDiffAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('diffset', 'status', 'binary',
                       ('source_file', 'source_revision'),
                       ('dest_file', 'dest_detail'),
                       'insert_count',
                       'delete_count',
                       'diff', 'parent_diff')
        }),
    )
    list_display = ('source_file', 'source_revision',
                    'dest_file', 'dest_detail')
    raw_id_fields = ('diffset',)
    readonly_fields = ('diff', 'parent_diff', 'insert_count', 'delete_count')

    def diff(self, filediff):
        return self._style_diff(filediff.diff)
    diff.label = _('Diff')
    diff.allow_tags = True

    def parent_diff(self, filediff):
        return self._style_diff(filediff.parent_diff)
    parent_diff.label = _('Parent diff')
    parent_diff.allow_tags = True

    def _style_diff(self, diff):
        # NOTE: Django wraps the contents in a <p>, but browsers will
        #       be sad about that, because it contains a <pre>. Chrome,
        #       for instance, will move it out into its own node. Be
        #       consistent and just make that happen for them.
        return '</p>%s<p>' % highlight(diff, DiffLexer(), HtmlFormatter())


class FileDiffInline(admin.StackedInline):
    model = FileDiff
    extra = 0


class DiffSetAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'revision', 'timestamp')
    raw_id_fields = ('history',)
    inlines = (FileDiffInline,)
    ordering = ('-timestamp',)


class DiffSetInline(admin.StackedInline):
    model = DiffSet
    extra = 0


class DiffSetHistoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'timestamp')
    inlines = (DiffSetInline,)
    ordering = ('-timestamp',)


admin.site.register(FileDiff, FileDiffAdmin)
admin.site.register(DiffSet, DiffSetAdmin)
admin.site.register(DiffSetHistory, DiffSetHistoryAdmin)
