from django.shortcuts import render, redirect
from django.contrib import messages

from note.models import Note


# Create your views here.
def home(request):
    '''
    Home page
    '''
    if not request.user.is_authenticated:
        messages.add_message(
            request,
            messages.ERROR,
            'You need to log in first!'
        )
        return redirect('login_view')
    context = {}
    # return all notes for user
    context['notes'] = Note.objects.filter(
        author=request.user).order_by('-updated_at')
    template_name = 'note/home.html'
    return render(request, template_name, context)


def note_view(request):
    '''
    Update single Note
    '''
    context = {}
    template_name = 'note/home.html'
    if request.htmx:
        data = request.POST
        # update Note
        if data['note_action'] == 'update':
            try:
                note = Note.objects.get(id=int(data.get('note_id')))
            except (Note.DoesNotExist, Note.MultipleObjectsReturned):
                messages.add_message(request, messages.ERROR,
                                     'Something went wrong...')
            # if Note exist - update it
            else:
                if note:
                    note.title = data.get('title')
                    note.content = data.get('content')
                    # set completed status
                    if (data.get('completed', None) is not None
                            and data.get('completed')) == 'on':
                        note.completed = True
                    else:
                        note.completed = False
                    note.save()
                    messages.add_message(request, messages.SUCCESS,
                                         'Your Note updated!')
        # create new Note
        if data['note_action'] == 'create':
            if (
                (data['title'] is None or len(data['title']) < 1)
                and (data['content'] is None or len(data['content']) < 1)
            ):
                messages.add_message(request, messages.ERROR,
                                     'Title or Content is required!')
            # if at least title or content provided - create Note
            else:
                new_note = Note.objects.create(title=data['title'],
                                               content=data['content'],
                                               author=request.user)
                # set completed status
                if (data.get('completed', None) is not None
                        and data.get('completed')) == 'on':
                    new_note.completed = True
                new_note.save()
                messages.add_message(request, messages.SUCCESS,
                                     'New Note added!')
    # return all notes for user
    context['notes'] = Note.objects.filter(
        author=request.user
    ).order_by('-updated_at')
    return render(request, template_name, context)


def delete_note_view(request, note_id):
    '''
    Delete single Note
    '''
    context = {}
    template_name = 'note/home.html'
    # delete Note
    if request.method == 'DELETE':
        try:
            note = Note.objects.get(id=note_id)
            note.delete()
            messages.add_message(request, messages.WARNING,
                                 'Your Note was deleted!')
        except (Note.DoesNotExist, Note.MultipleObjectsReturned):
            messages.add_message(request, messages.ERROR,
                                 'Something went wrong...')
    # return all notes for user
    context['notes'] = Note.objects.filter(
        author=request.user
    ).order_by('-updated_at')
    return render(request, template_name, context)


def bulk_notes_view(request):
    '''
    Bulk Notes actions
    '''
    context = {}
    template_name = 'note/home.html'
    if request.htmx:
        # get selected Notes ids
        selected_notes_ids_raw = request.POST.get('selected-notes-ids')
        selected_notes_ids = selected_notes_ids_raw.split(',')
        # get nptes action
        action = request.POST.get('bulk-notes-action')
        # bulk delete Notes
        if action == 'bulk_delete':
            for note_id in selected_notes_ids:
                try:
                    note = Note.objects.get(id=note_id)
                    note.delete()
                except (Note.DoesNotExist, Note.MultipleObjectsReturned):
                    messages.add_message(request, messages.ERROR,
                                         'Something went wrong...')
            messages.add_message(request, messages.WARNING,
                                 'Notes deleted!')
        # bulk change completes status for Notes
        else:
            for note_id in selected_notes_ids:
                try:
                    note = Note.objects.get(id=note_id)
                    if note.completed:
                        note.completed = False
                    else:
                        note.completed = True
                    note.save()
                except (Note.DoesNotExist, Note.MultipleObjectsReturned):
                    messages.add_message(request, messages.ERROR,
                                         'Something went wrong...')
            messages.add_message(request, messages.SUCCESS,
                                 'Notes updated!')
    # return all notes for user
    context['notes'] = Note.objects.filter(
        author=request.user
    ).order_by('-updated_at')
    return render(request, template_name, context)
