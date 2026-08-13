from jinja2 import Template

"""Production Jinja2 and HTML Component Renderer for EAOS Design System."""


class UIComponentEngine:
    """Renders standardized Tailwind CSS UI components."""

    BUTTON_TEMPLATE = Template(
        '<button type="{{ type }}" class="px-4 py-2 rounded-lg font-medium '
        "transition-colors duration-150 "
        '{% if variant == "primary" %}bg-cyan-600 hover:bg-cyan-500 text-white'
        '{% elif variant == "danger" %}bg-red-600 hover:bg-red-500 text-white'
        "{% else %}bg-slate-700 hover:bg-slate-600 text-slate-200{% endif %} "
        '{{ extra_classes }}">{{ label }}</button>'
    )

    CARD_TEMPLATE = Template(
        '<div class="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg '
        '{{ extra_classes }}">'
        '{% if title %}<h3 class="text-lg font-semibold text-slate-100 mb-2">'
        "{{ title }}</h3>{% endif %}"
        '<div class="text-sm text-slate-300">{{ content }}</div>'
        "</div>"
    )

    BADGE_TEMPLATE = Template(
        '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full '
        "text-xs font-semibold "
        '{% if status == "success" %}bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
        '{% elif status == "warning" %}bg-amber-500/10 text-amber-400 border border-amber-500/20'
        '{% elif status == "danger" %}bg-rose-500/10 text-rose-400 border border-rose-500/20'
        '{% else %}bg-slate-500/10 text-slate-400 border border-slate-500/20{% endif %}">'
        "{{ label }}</span>"
    )

    def render_button(
        self,
        label: str,
        variant: str = "primary",
        type: str = "button",
        extra_classes: str = "",
    ) -> str:
        """Renders a styled Tailwind CSS button."""
        return self.BUTTON_TEMPLATE.render(
            label=label,
            variant=variant,
            type=type,
            extra_classes=extra_classes,
        )

    def render_card(
        self,
        content: str,
        title: str | None = None,
        extra_classes: str = "",
    ) -> str:
        """Renders a styled Tailwind CSS card container."""
        return self.CARD_TEMPLATE.render(
            content=content,
            title=title,
            extra_classes=extra_classes,
        )

    def render_badge(self, label: str, status: str = "info") -> str:
        """Renders a styled status badge."""
        return self.BADGE_TEMPLATE.render(label=label, status=status)
