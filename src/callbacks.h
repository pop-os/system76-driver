#include <gtk/gtk.h>


void
on_mainWindow_destroy                  (GtkObject       *object,
                                        gpointer         user_data);

void
on_about_clicked                       (GtkButton       *button,
                                        gpointer         user_data);

void
on_close_clicked                       (GtkButton       *button,
                                        gpointer         user_data);

void
on_driverInstall_clicked               (GtkButton       *button,
                                        gpointer         user_data);

void
on_restore_clicked                     (GtkButton       *button,
                                        gpointer         user_data);
