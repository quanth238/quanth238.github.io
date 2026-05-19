// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-publications",
          title: "publications",
          description: "Selected research publications and manuscripts.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-projects",
          title: "projects",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "Academic CV, research experience, selected publications, teaching, software engineering experience, and technical skills.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-teaching",
          title: "teaching",
          description: "Teaching assistant work and course support.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "post-flow-matching-official-api",
        
          title: "Flow Matching: Official API",
        
        description: "Map toy code to the package.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/flow-matching-guide-part-6/";
          
        },
      },{id: "post-flow-matching-path-design",
        
          title: "Flow Matching: Path Design",
        
        description: "Compare two path schedules.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/flow-matching-guide-part-5/";
          
        },
      },{id: "post-flow-matching-endpoint-pairing",
        
          title: "Flow Matching: Endpoint Pairing",
        
        description: "Compare random and OT pairing.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/flow-matching-guide-part-4/";
          
        },
      },{id: "post-flow-matching-local-averages",
        
          title: "Flow Matching: Local Averages",
        
        description: "Average arrows into a field.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/flow-matching-guide-part-3/";
          
        },
      },{id: "post-flow-matching-ode-sampling",
        
          title: "Flow Matching: ODE Sampling",
        
        description: "Compare coarse and fine ODE steps.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/flow-matching-guide-part-2/";
          
        },
      },{id: "post-flow-matching-velocity-fields",
        
          title: "Flow Matching: Velocity Fields",
        
        description: "Train the basic velocity target.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/flow-matching-guide-part-1/";
          
        },
      },{id: "news-started-the-master-of-science-in-computer-science-at-vinuniversity-through-the-graduate-research-excellence-program",
          title: 'Started the Master of Science in Computer Science at VinUniversity through the Graduate...',
          description: "",
          section: "News",},{id: "news-gave-an-invited-talk-on-3d-gaussian-splatting-at-the-cair-monthly-reading-group-vinuniversity",
          title: 'Gave an invited talk on 3D Gaussian Splatting at the CAIR Monthly Reading...',
          description: "",
          section: "News",},{id: "news-launched-this-academic-portfolio-based-on-al-folio",
          title: 'Launched this academic portfolio based on al-folio.',
          description: "",
          section: "News",},{id: "teachings-data-mining-comp4040",
          title: 'Data Mining (COMP4040)',
          description: "Teaching assistant support for lab materials, lab sessions, and student projects.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/data-mining-comp4040/";
            },},{
        id: 'social-cv',
        title: 'CV',
        section: 'Socials',
        handler: () => {
          window.open("/assets/pdf/quan-tran-hong-cv.pdf", "_blank");
        },
      },{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%71%75%61%6E%74%68%32%33%38@%67%6D%61%69%6C.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/quanth238", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/quan2381", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=VZ0L3wIAAAAJ", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
