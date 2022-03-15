# run the containter
# docker run --name antora --rm --publish 35729:35729 --publish 2020:2020 --volume "$(pwd)":/preview/antora -d vshn/antora-preview:2.3.12 --antora=docs --style=vshn

group :documentation do
    # Rebuild documentation when modifying files
    guard :shell do
        watch(/(.*).adoc/) do
            `docker exec -it antora antora --cache-dir=/preview/public/.cache/antora /preview/playbook.yml`
        end
    end

    # Refresh browser when folder with HTML files changes
    guard :livereload do
        watch(/(.*).adoc/)
    end
end
