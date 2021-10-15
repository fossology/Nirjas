# Copyright (C) 2021 Aswin Murali (aswinmurali.co@gmail.com)
# Copyright (C) 2021 Gaurav Mishra <mishra.gaurav@siemens.com>
#
# SPDX-License-Identifier: LGPL-2.1-only
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Docker image for nirjas
# 
# Build
#   docker build -t nirjas .
#
# Run
#   docker run --rm -it nirjas <args>

FROM python:3.8-alpine as builder

WORKDIR /nirjas

COPY . .

RUN python3 -m pip wheel --wheel-dir wheels .

FROM python:3.8-alpine

ARG user=nirjas
ARG group=nirjas
ARG uid=1000
ARG gid=1000
ARG AGENT_HOME=/home/${user}

ENV AGENT_HOME ${AGENT_HOME}

RUN addgroup -g ${gid} ${group} \
 && adduser -h "${AGENT_HOME}" -u "${uid}" -G "${group}" -D "${user}"

WORKDIR "${AGENT_HOME}"

COPY --from=builder /nirjas/wheels/ .

RUN python -m pip install --prefix=/usr/local ./*.whl \
 && rm ./*.whl

USER nirjas

# Default command as intro text

ENTRYPOINT [ "nirjas" ]
CMD [ "-h" ]

LABEL \
    org.opencontainers.image.vendor="FOSSology" \
    org.opencontainers.image.title="Official Nirjas Docker image" \
    org.opencontainers.image.description="Image to run Nirjas without installing" \
    org.opencontainers.image.url="https://fossology.org" \
    org.opencontainers.image.source="https://github.com/fossology/Nirjas" \
    org.opencontainers.image.licenses="LGPL-2.1-only"
