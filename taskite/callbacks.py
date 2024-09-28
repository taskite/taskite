from django.db import models


class FileUploadCallback:
    def get_file_fields(self):
        return [
            field for field in self._meta.fields if isinstance(field, models.FileField)
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            pass
        else:
            has_file_fields = False
            self._original_file_fields = {}
            # Pre-save: Cache original file fields for existing instance
            if len(self.get_file_fields()) > 0:
                has_file_fields = True
                file_field_names = [field.name for field in self.get_file_fields()]
                original_instance = self.__class__.objects.only(
                    "pk", *file_field_names
                ).get(pk=self.pk)

                for field in self.get_file_fields():
                    original_file = getattr(original_instance, field.name)
                    if original_file:
                        self._original_file_fields[field.name] = original_file.name

            # Call the original save() method to actually save the instance
            super().save(*args, **kwargs)

            if has_file_fields:
                for field in self.get_file_fields():
                    current_file = getattr(self, field.name)
                    original_file_name = self._original_file_fields.get(field.name)

                    if current_file and current_file != original_file_name:
                        # New file uploaded or changed
                        print("New file uploaded or changed")
                    elif not current_file and original_file_name:
                        # File was removed
                        print("File was removed")
