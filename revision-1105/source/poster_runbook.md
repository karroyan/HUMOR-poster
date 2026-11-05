# revision-1105 reproduction

Run from the revision-1105 directory:

```bash
MPLCONFIGDIR=/tmp/humor-1105-mpl /usr/bin/python3 source/build_poster.py
/usr/bin/python3 source/verify_evidence.py
```

The first command builds HUMOR-poster-print.pdf, HUMOR-poster-preview.png, HUMOR-poster-editable.svg, HUMOR-poster-editable.pptx and HUMOR-poster.html. It reads assets/, fonts/ and source/poster.yaml. It uses the local copy of Paper2Poster's configuration loader; the module's original project license is included. No original output-folder paths or API keys are required for generation.

The verification command uses the shared paper at ../assets/Meme_NeurIPS_2026.pdf for its paper SHA-256 and the bundled evidence files for independent numeric/image checks. This matches the shared-paper arrangement used by revision-v5. If moving the revision alone, generation still works, while full paper verification needs that paper at the documented relative location.

Core copied artifacts are byte-identical to the user's latest source output; HTML only changes its outer version label. organization-validation.json records copied-file hashes and a separate temporary-directory rebuild test. The live copied artwork was not overwritten during that test.

Historical upstream evidence and its full validation report are preserved. Checks tied to the old output-directory backup ZIP were completed upstream and remain in export_validation_upstream.json; the organized verifier does not depend on that historical ZIP.
