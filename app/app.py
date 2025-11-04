import reflex as rx
from reflex_google_auth import google_oauth_provider, require_google_login, google_login
from .state import LocalAuthState, MyGoogleAuthState
from .states.admin_state import AdminState


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
        LocalAuthState.is_authenticated, authenticated_page(), auth_layout(login_form())
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Dashboard", href="/admin", class_name="p-4 hover:bg-gray-100 rounded-md"
        ),
        rx.el.a("Events", href="#", class_name="p-4 hover:bg-gray-100 rounded-md"),
        rx.el.a("Users", href="#", class_name="p-4 hover:bg-gray-100 rounded-md"),
        rx.el.a("Payments", href="#", class_name="p-4 hover:bg-gray-100 rounded-md"),
        rx.el.hr(),
        rx.el.button(
            "Logout",
            on_click=LocalAuthState.logout,
            class_name="w-full text-left p-4 hover:bg-gray-100 rounded-md",
        ),
        class_name="flex flex-col h-screen w-64 bg-white border-r border-gray-200 p-4 shadow-md",
    )


def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(), rx.el.main(content, class_name="flex-1 p-8"), class_name="flex"
    )


def authenticated_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.h1(
                f"Welcome, {LocalAuthState.authenticated_user['name']}!",
                class_name="text-2xl font-bold mb-6",
            ),
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
            ),
        )
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
            authenticated_page(),
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
app.add_page(index)
app.add_page(login, route="/login")
app.add_page(register, route="/register")
app.add_page(admin_page, route="/admin", on_load=AdminState.load_dashboard_data)