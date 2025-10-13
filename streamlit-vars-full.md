```markdown
Streamlit API catalog (best-effort)
==================================

This file lists commonly used public members of the `streamlit` module (widgets, layout
helpers, state management, caching, display helpers, and experimental APIs) with
short descriptions. This is a best-effort human-readable catalog — Streamlit evolves
and experimental names may change. For an exact, runtime list, use the runtime enum
command shown below.

Runtime enum (run locally in the project venv):

  python -c "import streamlit as st; print('\n'.join(sorted(dir(st))))"

Core page configuration
- st.set_page_config(page_title=None, page_icon=None, layout='centered', initial_sidebar_state='auto', menu_items=None)
  - Configure page title, icon, layout and sidebar initial state. Must be called once at top of script.

Text and markdown
- st.title(text)
- st.header(text)
- st.subheader(text)
- st.markdown(md, unsafe_allow_html=False)
- st.write(obj, *args, **kwargs)
- st.caption(text)
- st.code(code, language='')
- st.latex(expr)
- st.json(obj)
  - Basic text rendering and markup. `st.write` is polymorphic and accepts many types.

Status messages and alerts
- st.success(text), st.info(text), st.warning(text), st.error(text), st.exception(e)
  - Display contextual alerts to the user.

Media / display
- st.image(img, caption=None, use_column_width=False)
- st.audio(data, format=None)
- st.video(data)
- st.map(data)
- st.dataframe(data, width=None, height=None)
- st.table(data)
- st.metric(label, value, delta=None)
- st.plotly_chart(fig), st.altair_chart(chart), st.bokeh_chart(obj), st.pyplot(fig)
  - Display tabular data, metrics and charts using many backends.

Layout and containers
- st.container()
- st.columns(spec)  # returns column objects
- st.expander(label, expanded=False)
- st.sidebar  # module-like object to create sidebar widgets
- st.empty()  # placeholder to be updated later
- st.form(key=None) and st.form_submit_button(label)
  - Manage layout; `st.columns()` is used to place widgets side-by-side. `st.sidebar` mirrors top-level API.

Input widgets (single-value)
- st.button(label, key=None, on_click=None, args=None)
- st.checkbox(label, value=False, key=None)
- st.radio(label, options, index=0, key=None)
- st.selectbox(label, options, index=0, key=None)
- st.multiselect(label, options, default=None, key=None)
- st.slider(label, min_value=None, max_value=None, value=None, step=None, key=None)
- st.select_slider(label, options, value=None, key=None)
- st.number_input(label, min_value=None, max_value=None, value=None, step=None, key=None)
- st.text_input(label, value='', key=None)
- st.text_area(label, value='', key=None)
- st.date_input(label, value=None, key=None)
- st.time_input(label, value=None, key=None)
- st.file_uploader(label, type=None, accept_multiple_files=False, key=None)
- st.color_picker(label, value='#000000', key=None)
- st.download_button(label, data, file_name=None, mime=None, key=None)
  - Primary user input controls. Most accept `key` to store value in `st.session_state`.

State and session
- st.session_state (dict-like)
  - Persistent storage across reruns keyed by widget `key` or set manually. Initialize keys with defaults if missing.

Caching & resource management
- st.cache_data(func) / st.cache_resource(func)
  - Cache function return values; `cache_data` for small results, `cache_resource` for long-lived resources.

Progress & spinners
- st.progress(int)  # show progress bar
- st.spinner(text)  # context manager
- st.balloons()
- st.snow()
  - Feedback and loading indicators.

Advanced / experimental APIs (common)
- st.experimental_get_query_params(), st.experimental_set_query_params(**params)
- st.experimental_show(obj)
- st.experimental_singleton (older cache API; prefer cache_resource)
- st.session_state.sync()  # internal helpers
  - Experimental APIs may change across releases.

Utility & helpers
- st.beta_columns, st.beta_expander (legacy names; some older examples use them)
- st.echo()  # show code before execution
- st.pyplot() / st.altair_chart() etc. for specific plotting backends

Best practices notes
- Always provide `key` arguments when you need stable `st.session_state` entries across widget re-creation.
- Use `st.number_input` or `st.slider` to enforce numeric ranges instead of manual clamping on button callbacks.
- Initialize `st.session_state` keys with default values only when absent, e.g.:

    if 'my_key' not in st.session_state:
        st.session_state['my_key'] = default_value

- Prefer `st.cache_data` / `st.cache_resource` (or the newest caching API) to memoize expensive computation or create heavy resources once.

If you want an exact, machine-produced list of every attribute exposed by the installed version of Streamlit in this environment, run:

  python - <<PY
import streamlit as st
for name in sorted(dir(st)):
    print(name)
PY

This will show everything currently available on the `st` module (widgets, helpers, experimental names).

```