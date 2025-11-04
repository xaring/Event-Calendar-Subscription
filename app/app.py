import reflex as rx
from reflex_google_auth import google_oauth_provider, require_google_login, google_login
from .state import LocalAuthState, MyGoogleAuthState
from .states.admin_state import AdminState
from .states.event_state import EventState
from .states.group_state import GroupState


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Login", class_name="text-3xl font-bold text-gray-800 mb-6 text-center"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label("Email", class_name="text-sm font-medium text-gray-600"),
                rx.el.input(
                    name="email",
                    type="email",
                    placeholder="you@example.com",
                    class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label("Password", class_name="text-sm font-medium text-gray-600"),
                rx.el.input(
                    name="password",
                    type="password",
                    placeholder="••••••••",
                    class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                ),
                class_name="mb-6",
            ),
            rx.cond(
                LocalAuthState.error_message != "",
                rx.el.div(
                    LocalAuthState.error_message,
                    class_name="bg-red-100 text-red-700 p-3 rounded-lg mb-4 text-sm",
                ),
                None,
            ),
            rx.el.button(
                "Sign In",
                type="submit",
                class_name="w-full bg-orange-500 text-white py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors shadow-md",
            ),
            on_submit=LocalAuthState.login,
            reset_on_submit=False,
            class_name="w-full",
        ),
        rx.el.div("or", class_name="text-center text-gray-500 my-4"),
        google_login(on_success=MyGoogleAuthState.on_success, class_name="w-full"),
        rx.el.p(
            "Don't have an account? ",
            rx.el.a(
                "Sign up",
                href="/register",
                class_name="text-orange-500 hover:underline",
            ),
            class_name="text-center text-sm text-gray-600 mt-6",
        ),
        class_name="max-w-md w-full bg-white p-8 rounded-2xl shadow-lg border border-gray-200",
    )


def register_form() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Create Account",
            class_name="text-3xl font-bold text-gray-800 mb-6 text-center",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Full Name", class_name="text-sm font-medium text-gray-600"
                ),
                rx.el.input(
                    name="name",
                    placeholder="John Doe",
                    class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label("Email", class_name="text-sm font-medium text-gray-600"),
                rx.el.input(
                    name="email",
                    type="email",
                    placeholder="you@example.com",
                    class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label("Password", class_name="text-sm font-medium text-gray-600"),
                rx.el.input(
                    name="password",
                    type="password",
                    placeholder="••••••••",
                    class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Confirm Password", class_name="text-sm font-medium text-gray-600"
                ),
                rx.el.input(
                    name="confirm_password",
                    type="password",
                    placeholder="••••••••",
                    class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                ),
                class_name="mb-6",
            ),
            rx.cond(
                LocalAuthState.error_message != "",
                rx.el.div(
                    LocalAuthState.error_message,
                    class_name="bg-red-100 text-red-700 p-3 rounded-lg mb-4 text-sm",
                ),
                None,
            ),
            rx.el.button(
                "Sign Up",
                type="submit",
                class_name="w-full bg-orange-500 text-white py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors shadow-md",
            ),
            on_submit=LocalAuthState.register,
            reset_on_submit=False,
            class_name="w-full",
        ),
        rx.el.p(
            "Already have an account? ",
            rx.el.a(
                "Sign in", href="/login", class_name="text-orange-500 hover:underline"
            ),
            class_name="text-center text-sm text-gray-600 mt-6",
        ),
        class_name="max-w-md w-full bg-white p-8 rounded-2xl shadow-lg border border-gray-200",
    )


def auth_layout(component: rx.Component) -> rx.Component:
    return google_oauth_provider(
        rx.el.main(
            rx.el.div(
                component,
                class_name="flex items-center justify-center min-h-screen p-4",
            ),
            class_name="bg-gray-50 font-['Open_Sans']",
        )
    )


def index() -> rx.Component:
    return rx.cond(
        LocalAuthState.is_authenticated,
        dashboard_layout(home_page()),
        auth_layout(login_form()),
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a("Dashboard", href="/", class_name="font-semibold text-lg"),
            class_name="p-4 border-b",
        ),
        rx.el.nav(
            rx.el.a(
                rx.icon("home", class_name="w-5 h-5"),
                "Home",
                href="/",
                class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
            rx.el.a(
                rx.icon("calendar", class_name="w-5 h-5"),
                "Events",
                href="/events",
                class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
            rx.el.a(
                rx.icon("users", class_name="w-5 h-5"),
                "Groups",
                href="/groups",
                class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
            rx.el.a(
                rx.icon("calendar-check", class_name="w-5 h-5"),
                "My Events",
                href="/my-events",
                class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
            rx.el.a(
                rx.icon("lock", class_name="w-5 h-5"),
                "Change Password",
                href="/change-password",
                class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
            rx.cond(
                LocalAuthState.is_admin,
                rx.el.div(
                    rx.el.h3(
                        "Admin",
                        class_name="font-semibold text-sm text-gray-500 px-3 mt-4 mb-2",
                    ),
                    rx.el.a(
                        rx.icon("shield", class_name="w-5 h-5"),
                        "Admin Dashboard",
                        href="/admin",
                        class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
                    ),
                    rx.el.a(
                        rx.icon("calendar-plus", class_name="w-5 h-5"),
                        "Manage Events",
                        href="/admin/events",
                        class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
                    ),
                    rx.el.a(
                        rx.icon("user-plus", class_name="w-5 h-5"),
                        "Manage Groups",
                        href="/admin/groups",
                        class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
                    ),
                ),
                None,
            ),
            class_name="grid items-start px-4 text-sm font-medium",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("log-out", class_name="w-5 h-5 mr-2"),
                "Logout",
                on_click=LocalAuthState.logout,
                class_name="flex items-center w-full text-left p-3 hover:bg-gray-100 rounded-lg",
            ),
            class_name="mt-auto p-4 border-t",
        ),
        class_name="flex flex-col h-screen w-64 bg-white border-r border-gray-200 shadow-md",
    )


def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(), rx.el.main(content, class_name="flex-1 p-8"), class_name="flex"
    )


def home_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            f"Welcome, {LocalAuthState.authenticated_user['name']}!",
            class_name="text-2xl font-bold mb-6",
        ),
        rx.el.p("This is your dashboard."),
    )


def change_password_page() -> rx.Component:
    return rx.cond(
        LocalAuthState.is_authenticated,
        dashboard_layout(
            rx.el.div(
                rx.el.h2("Change Password", class_name="text-xl font-semibold mb-4"),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Current Password",
                            class_name="text-sm font-medium text-gray-600",
                        ),
                        rx.el.input(
                            name="current_password",
                            type="password",
                            class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "New Password",
                            class_name="text-sm font-medium text-gray-600",
                        ),
                        rx.el.input(
                            name="new_password",
                            type="password",
                            class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Confirm New Password",
                            class_name="text-sm font-medium text-gray-600",
                        ),
                        rx.el.input(
                            name="confirm_new_password",
                            type="password",
                            class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        LocalAuthState.error_message != "",
                        rx.el.div(
                            LocalAuthState.error_message,
                            class_name="bg-red-100 text-red-700 p-3 rounded-lg mb-4 text-sm",
                        ),
                        None,
                    ),
                    rx.cond(
                        LocalAuthState.success_message != "",
                        rx.el.div(
                            LocalAuthState.success_message,
                            class_name="bg-green-100 text-green-700 p-3 rounded-lg mb-4 text-sm",
                        ),
                        None,
                    ),
                    rx.el.button(
                        "Change Password",
                        type="submit",
                        class_name="w-full bg-orange-500 text-white py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors shadow-md",
                    ),
                    on_submit=LocalAuthState.change_password,
                    reset_on_submit=False,
                    class_name="max-w-md",
                ),
                class_name="p-6 bg-white rounded-lg shadow-sm border border-gray-200",
            )
        ),
        auth_layout(login_form()),
    )


def admin_page() -> rx.Component:
    return rx.cond(
        LocalAuthState.is_authenticated,
        rx.cond(
            LocalAuthState.is_admin,
            dashboard_layout(
                rx.el.div(
                    rx.el.h1("Admin Dashboard", class_name="text-2xl font-bold mb-4"),
                    rx.el.div(
                        admin_content(),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                )
            ),
            dashboard_layout(home_page()),
        ),
        auth_layout(login_form()),
    )


def login() -> rx.Component:
    return auth_layout(login_form())


def register() -> rx.Component:
    return auth_layout(register_form())


def admin_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Users", class_name="text-xl font-semibold mb-4"),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("ID", class_name="px-4 py-2"),
                        rx.el.th("Name", class_name="px-4 py-2"),
                        rx.el.th("Email", class_name="px-4 py-2"),
                        rx.el.th("Role", class_name="px-4 py-2"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        AdminState.users,
                        lambda user: rx.el.tr(
                            rx.el.td(user.id, class_name="border px-4 py-2"),
                            rx.el.td(user.name, class_name="border px-4 py-2"),
                            rx.el.td(user.email, class_name="border px-4 py-2"),
                            rx.el.td(user.role, class_name="border px-4 py-2"),
                        ),
                    )
                ),
                class_name="w-full text-left table-auto",
            ),
            class_name="bg-white p-4 rounded-lg shadow",
        ),
        rx.el.div(
            rx.el.h2("Groups", class_name="text-xl font-semibold mb-4"),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("ID", class_name="px-4 py-2"),
                        rx.el.th("Name", class_name="px-4 py-2"),
                        rx.el.th("Description", class_name="px-4 py-2"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        AdminState.groups,
                        lambda group: rx.el.tr(
                            rx.el.td(group.id, class_name="border px-4 py-2"),
                            rx.el.td(group.name, class_name="border px-4 py-2"),
                            rx.el.td(group.description, class_name="border px-4 py-2"),
                        ),
                    )
                ),
                class_name="w-full text-left table-auto",
            ),
            class_name="bg-white p-4 rounded-lg shadow",
        ),
        rx.el.div(
            rx.el.h2("Events", class_name="text-xl font-semibold mb-4"),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("ID", class_name="px-4 py-2"),
                        rx.el.th("Title", class_name="px-4 py-2"),
                        rx.el.th("Start Time", class_name="px-4 py-2"),
                        rx.el.th("End Time", class_name="px-4 py-2"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        AdminState.events,
                        lambda event: rx.el.tr(
                            rx.el.td(event.id, class_name="border px-4 py-2"),
                            rx.el.td(event.title, class_name="border px-4 py-2"),
                            rx.el.td(
                                event.start_time.to_string(),
                                class_name="border px-4 py-2",
                            ),
                            rx.el.td(
                                event.end_time.to_string(),
                                class_name="border px-4 py-2",
                            ),
                        ),
                    )
                ),
                class_name="w-full text-left table-auto",
            ),
            class_name="bg-white p-4 rounded-lg shadow",
        ),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)


def events_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.h1("Events", class_name="text-2xl font-bold mb-6"),
            rx.el.div(
                rx.foreach(
                    EventState.events,
                    lambda event: rx.el.div(
                        rx.el.h2(event.title, class_name="font-semibold text-lg"),
                        rx.el.p(event.description, class_name="text-sm text-gray-600"),
                        rx.el.div(
                            rx.el.span(
                                f"From: {event.start_time.to_string()}",
                                class_name="text-xs",
                            ),
                            rx.el.span(
                                f"To: {event.end_time.to_string()}",
                                class_name="text-xs",
                            ),
                            class_name="flex justify-between text-gray-500 mt-2",
                        ),
                        rx.el.button(
                            "Sign Up",
                            on_click=lambda: EventState.signup_for_event(event.id),
                            class_name="mt-4 w-full bg-blue-500 text-white py-2 rounded-lg font-semibold hover:bg-blue-600 transition-colors",
                        ),
                        class_name="bg-white p-4 rounded-lg shadow-sm border flex flex-col justify-between",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
        )
    )


def my_events_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.h1("My Events", class_name="text-2xl font-bold mb-6"),
            rx.cond(
                EventState.my_events,
                rx.el.div(
                    rx.foreach(
                        EventState.my_events,
                        lambda event: rx.el.div(
                            rx.el.h2(event.title, class_name="font-semibold text-lg"),
                            rx.el.p(
                                event.description, class_name="text-sm text-gray-600"
                            ),
                            rx.el.div(
                                rx.el.span(
                                    f"From: {event.start_time.to_string()}",
                                    class_name="text-xs",
                                ),
                                rx.el.span(
                                    f"To: {event.end_time.to_string()}",
                                    class_name="text-xs",
                                ),
                                class_name="flex justify-between text-gray-500 mt-2",
                            ),
                            rx.el.button(
                                "Cancel Signup",
                                on_click=lambda: EventState.cancel_signup(event.id),
                                class_name="mt-4 w-full bg-red-500 text-white py-2 rounded-lg font-semibold hover:bg-red-600 transition-colors",
                            ),
                            class_name="bg-white p-4 rounded-lg shadow-sm border flex flex-col justify-between",
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.el.p("You have not signed up for any events yet."),
            ),
        )
    )


def admin_events_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.h1("Manage Events", class_name="text-2xl font-bold mb-6"),
            rx.el.div(
                rx.el.div(
                    rx.el.h2("Create Event", class_name="text-xl font-semibold mb-4"),
                    rx.el.form(
                        rx.el.input(
                            name="title",
                            placeholder="Title",
                            class_name="w-full p-2 border rounded mb-2",
                        ),
                        rx.el.textarea(
                            name="description",
                            placeholder="Description",
                            class_name="w-full p-2 border rounded mb-2",
                        ),
                        rx.el.input(
                            name="start_time",
                            type="datetime-local",
                            class_name="w-full p-2 border rounded mb-2",
                        ),
                        rx.el.input(
                            name="end_time",
                            type="datetime-local",
                            class_name="w-full p-2 border rounded mb-2",
                        ),
                        rx.el.select(
                            rx.el.option("No Group", value=""),
                            rx.foreach(
                                EventState.groups,
                                lambda group: rx.el.option(group.name, value=group.id),
                            ),
                            name="group_id",
                            class_name="w-full p-2 border rounded mb-4",
                        ),
                        rx.el.button(
                            "Create Event",
                            type="submit",
                            class_name="w-full bg-orange-500 text-white py-2 rounded-lg font-semibold hover:bg-orange-600",
                        ),
                        on_submit=EventState.create_event,
                        reset_on_submit=True,
                        class_name="mb-8 p-4 bg-white rounded-lg shadow-sm border",
                    ),
                ),
                rx.el.div(
                    rx.el.h2(
                        "Existing Events", class_name="text-xl font-semibold mb-4"
                    ),
                    rx.foreach(
                        EventState.events,
                        lambda event: rx.el.div(
                            rx.el.div(
                                rx.el.h3(event.title, class_name="font-semibold"),
                                rx.el.p(
                                    f"{event.start_time.to_string()} - {event.end_time.to_string()}",
                                    class_name="text-sm text-gray-500",
                                ),
                            ),
                            rx.el.button(
                                "Delete",
                                on_click=lambda: EventState.delete_event(event.id),
                                class_name="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600",
                            ),
                            class_name="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm border mb-2",
                        ),
                    ),
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
        )
    )


def admin_groups_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.h1("Manage Groups", class_name="text-2xl font-bold mb-6"),
            rx.el.div(
                rx.el.div(
                    rx.el.h2("Create Group", class_name="text-xl font-semibold mb-4"),
                    rx.el.form(
                        rx.el.input(
                            name="name",
                            placeholder="Group Name",
                            class_name="w-full p-2 border rounded mb-2",
                        ),
                        rx.el.textarea(
                            name="description",
                            placeholder="Description",
                            class_name="w-full p-2 border rounded mb-4",
                        ),
                        rx.el.button(
                            "Create Group",
                            type="submit",
                            class_name="w-full bg-orange-500 text-white py-2 rounded-lg font-semibold hover:bg-orange-600",
                        ),
                        on_submit=GroupState.create_group,
                        reset_on_submit=True,
                        class_name="mb-8 p-4 bg-white rounded-lg shadow-sm border",
                    ),
                ),
                rx.el.div(
                    rx.el.h2(
                        "Existing Groups", class_name="text-xl font-semibold mb-4"
                    ),
                    rx.foreach(
                        GroupState.groups,
                        lambda group: rx.el.div(
                            rx.el.div(
                                rx.el.h3(group.name, class_name="font-semibold"),
                                rx.el.p(
                                    group.description,
                                    class_name="text-sm text-gray-500",
                                ),
                            ),
                            rx.el.button(
                                "Delete",
                                on_click=lambda: GroupState.delete_group(group.id),
                                class_name="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600",
                            ),
                            class_name="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm border mb-2",
                        ),
                    ),
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
        )
    )


def groups_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.h1("My Groups", class_name="text-2xl font-bold mb-6"),
            rx.cond(
                GroupState.user_groups,
                rx.el.div(
                    rx.foreach(
                        GroupState.user_groups,
                        lambda group: rx.el.div(
                            rx.el.h2(group.name, class_name="font-semibold text-lg"),
                            rx.el.p(
                                group.description, class_name="text-sm text-gray-600"
                            ),
                            class_name="bg-white p-4 rounded-lg shadow-sm border",
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                ),
                rx.el.p("You are not a member of any groups yet."),
            ),
        )
    )


app.add_page(index)
app.add_page(login, route="/login")
app.add_page(register, route="/register")
app.add_page(admin_page, route="/admin", on_load=AdminState.load_dashboard_data)
app.add_page(change_password_page, route="/change-password")
app.add_page(events_page, route="/events", on_load=EventState.load_events)
app.add_page(groups_page, route="/groups", on_load=GroupState.load_user_groups)
app.add_page(my_events_page, route="/my-events", on_load=EventState.load_my_events)
app.add_page(admin_events_page, route="/admin/events", on_load=EventState.load_events)
app.add_page(admin_groups_page, route="/admin/groups", on_load=GroupState.load_groups)