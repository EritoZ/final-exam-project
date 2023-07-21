class OwnerAddMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)
