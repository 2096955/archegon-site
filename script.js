const header = document.querySelector("[data-header]");
const leadForm = document.querySelector("#lead-form");
const formStatus = document.querySelector("[data-form-status]");

const syncHeader = () => {
  if (!header) return;
  header.dataset.scrolled = window.scrollY > 16 ? "true" : "false";
};

const trackEvent = (name, props = {}) => {
  if (!name || typeof window.plausible !== "function") return;
  window.plausible(name, { props });
};

const formatLeadEmail = (form) => {
  const data = new FormData(form);
  const fields = {
    intent: data.get("intent"),
    audience: data.get("audience"),
    name: data.get("name"),
    email: data.get("email"),
    organisation: data.get("organisation") || "Not provided",
    message: data.get("message"),
    newsletter: data.get("newsletter") ? "Yes" : "No",
  };

  const subject = `Archegon enquiry - ${fields.intent}`;
  const body = [
    `Intent: ${fields.intent}`,
    `Audience: ${fields.audience}`,
    `Name: ${fields.name}`,
    `Email: ${fields.email}`,
    `Organisation: ${fields.organisation}`,
    `Newsletter opt-in: ${fields.newsletter}`,
    "",
    "Message:",
    fields.message,
    "",
    "Consent: I consent to Archegon using this information to respond to my enquiry.",
    "",
    "Legal note: this message is an expression of interest only and is not an offer or invitation to invest.",
  ].join("\n");

  return `mailto:hello@archegon.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
};

syncHeader();
window.addEventListener("scroll", syncHeader, { passive: true });

document.querySelectorAll("[data-analytics-event]").forEach((element) => {
  element.addEventListener("click", () => {
    trackEvent(element.dataset.analyticsEvent, {
      href: element.getAttribute("href") || "",
      label: element.textContent.trim(),
    });
  });
});

if (leadForm) {
  leadForm.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!leadForm.reportValidity()) return;

    const mailto = formatLeadEmail(leadForm);
    trackEvent("Form: Lead mailto opened", {
      intent: new FormData(leadForm).get("intent") || "",
    });

    if (formStatus) {
      formStatus.textContent = "Opening your email client so you can review and send the enquiry.";
    }

    window.location.href = mailto;
  });
}
